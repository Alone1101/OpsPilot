from sqlalchemy.orm import Session
from models import Order, OrderStatus, CancelOrderResponse
from services.order_service import get_order_by_id, cancel_order

def get_order_tool(db: Session, order_id: str) -> Order:
    order = get_order_by_id(
        db = db,
        order_id = order_id
    )

    return Order(
        id = order.id,
        customer_id = order.customer_id,
        status = OrderStatus(order.status),
        total_amount = order.total_amount
    )

def cancel_order_tool(db: Session, order_id: str) -> CancelOrderResponse:
    return cancel_order(
        db = db,
        order_id = order_id
    )