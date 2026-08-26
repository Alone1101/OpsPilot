from typing import Callable
from sqlalchemy.orm import Session
from tools.order_tools import get_order_tool, cancel_order_tool, get_tracking_status_tool, check_refund_eligibility_tool, issue_refund_tool, escalate_case_tool
from exceptions import UnkownToolError, InvalidToolArgumentsError

TOOL_REGISTRY: dict[str, Callable] = {
    "get_order": get_order_tool,
    "cancel_order": cancel_order_tool,
    "get_tracking_status": get_tracking_status_tool,
    "check_refund_eligibility": check_refund_eligibility_tool,
    "issue_refund": issue_refund_tool,
    "escalate_case": escalate_case_tool
}

REQUIRED_ARGUMENTS = {
    "get_order": ["order_id"],
    "get_tracking_status": ["order_id"],
    "cancel_order": ["order_id"],
    "check_refund_eligibility": ["order_id"],
    "issue_refund": ["order_id", "amount"],
    "escalate_case": ["order_id"],
}

def execute_tool(db: Session, tool_name: str, arguments: dict):
    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        raise UnkownToolError(f"Unkown tool: {tool_name}")

    required = REQUIRED_ARGUMENTS.get(tool_name, [])

    missing = [argument 
               for argument in required 
               if arguments.get(argument) is None]

    if missing:
        raise InvalidToolArgumentsError(
            f"Missing required arguments for {tool_name}: "
            f"{', '.join(missing)}"
        )

    return tool(
        db = db,
        **arguments
    )