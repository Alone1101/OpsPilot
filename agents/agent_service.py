from sqlalchemy.orm import Session
from models import PolicyAgentResponse, ToolAgentResponse 
from agents.graph import build_agent_graph
from exceptions import OpsPilotError


def process_message(message: str, db: Session) -> PolicyAgentResponse | ToolAgentResponse:
    graph = build_agent_graph(db)

    try:
        state = graph.invoke({"message": message})

    except OpsPilotError as error:
        return ToolAgentResponse(
            tool = "system",
            error = str(error)
        )

    if "answer" in state:
        return PolicyAgentResponse(answer = state["answer"])

    return ToolAgentResponse(
        tool = state["tool"],
        result = state.get("result"),
        error = state.get("error")
    )