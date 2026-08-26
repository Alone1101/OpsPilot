from typing import TypedDict, Any
from sqlalchemy.orm import Session
from langgraph.graph import StateGraph, START, END
from models import RequestType
from services.rag_service import answer_policy_question
from tools.registry import execute_tool
from exceptions import OpsPilotError, EscalationRequiredError
from services.llm_service import decide_tool, classify_request

class AgentState(TypedDict, total = False):
    message: str
    request_type: RequestType
    tool: str
    arguments: dict[str, Any]
    result: dict[str, Any]
    answer: str
    error: str
    requires_escalation: bool

# Supporting functions
def classify_node(state: AgentState):
    classification = classify_request(state["message"])

    return {"request_type": classification.request_type}

def decide_action_node(state: AgentState):
    decision = decide_tool(state["message"])

    arguments = {"order_id": decision.order_id}

    if decision.amount is not None:
        arguments["amount"] = decision.amount

    if decision.reason is not None:
        arguments["reason"] = decision.reason

    if decision.priority is not None:
        arguments["priority"] = decision.priority

    return{
        "tool": decision.tool,
        "arguments": arguments
    }

# Routing logics
def route_after_classification(state: AgentState):
    if state["request_type"] == RequestType.POLICY_QUESTION:
        return "policy"

    return "action"

def route_after_execution(state: AgentState):
    if state.get("requires_escalation"):
        return "escalate"

    return "end"

# Actual agent graph
def build_agent_graph(db: Session):

    def policy_node(state: AgentState):
        answer = answer_policy_question(
            db = db,
            question = state["message"]
        )
        return{"answer": answer}

    def execute_action_node(state: AgentState):
        try:
            result = execute_tool(
                db = db,
                tool_name = state["tool"],
                arguments = state["arguments"]
            )

            return {
                "result": result.model_dump(),
                "requires_escalation": False
            }

        except EscalationRequiredError as error:
            return {
                "requires_escalation": True,
                "error": str(error)
            }

        except OpsPilotError as error:
            return {
                "requires_escalation": False,
                "error": str(error)
            }

    def escalate_node(state: AgentState):
        result = execute_tool(
            db = db,
            tool_name = "escalate_case",
            arguments = {
                "order_id": state["arguments"]["order_id"],
                "reason": state.get("error", "Human review required"),
                "priority": "HIGH"
            }
        )

        return {
            "tool": "escalate_case",
            "result": result.model_dump(),
            "error": None
        }

    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)

    graph.add_node("policy", policy_node)

    graph.add_node("decide_action", decide_action_node)

    graph.add_node("execute_action", execute_action_node)

    graph.add_node("escalate", escalate_node)

    graph.add_edge(START, "classify")

    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {
            "policy": "policy",
            "action": "decide_action"
        }
    )

    graph.add_edge("policy", END)

    graph.add_edge("decide_action", "execute_action")

    graph.add_conditional_edges(
        "execute_action",
        route_after_execution,
        {
            "escalate": "escalate",
            "end": END
        }
    )

    graph.add_edge("escalate", END)

    return graph.compile()