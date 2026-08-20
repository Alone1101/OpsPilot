from sqlalchemy.orm import Session
from models import ToolResponse
from tools.registry import execute_tool
from agents.gemini_client import decide_tool


def process_message(message: str, db: Session) -> ToolResponse:
    decision = decide_tool(message)

    arguments = {"order_id": decision.order_id}

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