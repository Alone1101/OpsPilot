from models import Order, CancelOrderResponse
from services.order_service import get_order_by_id, cancel_order

def get_order_tool(orders: dict[str, Order], order_id: str) -> Order:
    return get_order_by_id(
        orders = orders,
        order_id = order_id,
    )

def cancel_order_tool(orders: dict[str, Order], order_id: str) -> CancelOrderResponse:
    return cancel_order(
        orders = orders,
        order_id = order_id
    )