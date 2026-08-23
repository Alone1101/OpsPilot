from sqlalchemy.orm import Session
from models import RequestType, PolicyAgentResponse, ToolAgentResponse 
from services.rag_service import answer_policy_question
from tools.registry import execute_tool
from exceptions import OpsPilotError
from agents.gemini_client import decide_tool, classify_request


def process_message(message: str, db: Session) -> PolicyAgentResponse | ToolAgentResponse:
    classification = classify_request(message)

    if classification.requestType == RequestType.POLICY_QUESTION:
        answer = answer_policy_question(
            db = db,
            question = message
        )

        return PolicyAgentResponse(
            answer = answer
        )
    
    decision = decide_tool(message)

    arguments = {"order_id": decision.order_id}

    if decision.amount is not None:
        arguments["amount"] = decision.amount

    if decision.reason is not None:
        arguments["reason"] = decision.reason

    if decision.priority is not None:
        arguments["priority"] = decision.priority

    try:
        result = execute_tool(
            db = db,
            tool_name = decision.tool,
            arguments = arguments
        )

        return ToolAgentResponse(
            tool = decision.tool,
            result = result.model_dump()
        )

    except OpsPilotError as error:
        return ToolAgentResponse(
            tool = decision.tool,
            error = str(error)
        )