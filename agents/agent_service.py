from models import Order, ToolResponse
from tools.registry import execute_tool
from agents.gemini_client import decide_tool


def process_message(message: str, orders: dict[str, Order]) -> ToolResponse:
    decision = decide_tool(message)

    arguments = {"order_id": decision.order_id}

    result = execute_tool(
        orders = orders,
        tool_name = decision.tool,
        arguments = arguments
    )

    return ToolResponse(
        success = True,
        tool = decision.tool,
        result = result.model_dump()
    )