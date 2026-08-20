from sqlalchemy.orm import Session
from models import ToolResponse
from tools.registry import execute_tool
from exceptions import OpsPilotError
from agents.gemini_client import decide_tool


def process_message(message: str, db: Session) -> ToolResponse:
    decision = decide_tool(message)

    arguments = {"order_id": decision.order_id}

    if decision.amount is not None:
        arguments["amount"] = decision.amount

    try:
        result = execute_tool(
            db = db,
            tool_name = decision.tool,
            arguments = arguments
        )

        return ToolResponse(
            success = True,
            tool = decision.tool,
            result = result.model_dump()
        )

    except OpsPilotError as error:
        return ToolResponse(
            success = False,
            tool = decision.tool,
            error = str(error)
        )