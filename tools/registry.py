from typing import Callable
from sqlalchemy.orm import Session
from tools.order_tools import get_order_tool, cancel_order_tool
from exceptions import UnkownToolError

TOOL_REGISTRY: dict[str, Callable] = {
    "get_order": get_order_tool,
    "cancel_order": cancel_order_tool
}

def execute_tool(db: Session, tool_name: str, arguments: dict):
    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        raise UnkownToolError(f"Unkown tool: {tool_name}")

    return tool(
        db = db,
        **arguments
    )