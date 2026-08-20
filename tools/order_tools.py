from sqlalchemy.orm import Session
from models import Order, OrderStatus, CancelOrderResponse, TrackingResponse, RefundEligibilityResponse, RefundResponse
from services.order_service import get_order_by_id, cancel_order, get_tracking_status, check_refund_eligibility, issue_refund

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

def get_tracking_status_tool(db: Session, order_id: str) -> TrackingResponse:
    return get_tracking_status(
        db = db,
        order_id = order_id
    )

def check_refund_eligibility_tool(db: Session, order_id: str) -> RefundEligibilityResponse:
    return check_refund_eligibility(
        db = db,
        order_id = order_id
    )

def issue_refund_tool(db: Session, order_id: str, amount: float) -> RefundResponse:
    return issue_refund(
        db = db,
        order_id = order_id,
        amount = amount
    )