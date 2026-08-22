from sqlalchemy.orm import Session
from models import OrderStatus, CancelOrderResponse, TrackingResponse, RefundEligibilityResponse, RefundResponse, EscalationResponse
from db_models import OrderDB, RefundDB, EscalationDB
from exceptions import OrderNotFoundError, InvalidOrderActionError


def get_order_by_id(db: Session, order_id: str) -> OrderDB:
    order = db.get(OrderDB, order_id)

    if order is None:
        raise OrderNotFoundError(
            f"Order {order_id} not found"
        )

    return order


def cancel_order(db: Session, order_id: str) -> CancelOrderResponse:
    order = get_order_by_id(
        db = db,
        order_id = order_id,
    )

    if order.status != OrderStatus.PROCESSING.value:
        raise InvalidOrderActionError(
            f"Order cannot be cancelled while status is {order.status}"
        )

    order.status = OrderStatus.CANCELLED.value

    db.commit()
    db.refresh(order)

    return CancelOrderResponse(
        order_id = order.id,
        status = OrderStatus(order.status),
        message = "Order cancelled successfully"
    )

def get_tracking_status(db: Session, order_id: str) -> TrackingResponse:
    order = get_order_by_id(
        db = db,
        order_id = order_id
    )

    match order.status:
        case "DELIVERED":
            message = "Order has been delivered."

        case "SHIPPED":
            message = "Order is currently in transit."

        case "PROCESSING":
            message = "Order has not shipped yet."

        case "CANCELLED":
            message = "Order was cancelled."

        case _:
            message = "Unkown order status."

    return TrackingResponse(
        order_id = order.id,
        status = order.status,
        message = message
    )

def check_refund_eligibility(db: Session, order_id: str) -> RefundEligibilityResponse:
    order = get_order_by_id(
            db = db,
            order_id = order_id
        )

    match order.status:
        case "CANCELLED":
            return RefundEligibilityResponse(
                order_id = order.id,
                eligible = True,
                reason = "Cancelled orders are eligible for refund."
            )

        case "DELIVERED":
            return RefundEligibilityResponse(
            order_id = order.id,
            eligible = False,
            reason = "Delivered orders require return or delivery-issue review."
        )

        case "SHIPPED":
            return RefundEligibilityResponse(
            order_id = order.id,
            eligible = False,
            reason = "Shipped orders cannot be automatically refunded."
        )

        case _:
            return RefundEligibilityResponse(
                order_id = order.id,
                eligible = False,
                reason = "Order is not currently eligible for refund."
            )

def issue_refund(db: Session, order_id: str, amount: float) -> RefundResponse | EscalationResponse:
    order = get_order_by_id(
        db = db,
        order_id = order_id
    )

    if amount <= 0:
        raise InvalidOrderActionError("Refund amount must be greater than 0.")

    if amount > order.total_amount:
        raise InvalidOrderActionError("Refund amount cannot exceed order total.")

    if amount > 250:
        return escalate_case(
            db = db,
            order_id = order_id,
            reason = f"Refund request of RM{amount:.2f} exceeds autonomous limit",
            priority = "HIGH"
        )

    eligibility = check_refund_eligibility(
        db = db,
        order_id = order_id
    )

    if not eligibility.eligible:
        raise InvalidOrderActionError(eligibility.reason)

    existing_refund = (
        db.query(RefundDB).filter(RefundDB.order_id == order_id).first()
    )

    if existing_refund is not None:
        raise InvalidOrderActionError("A refund has already been issued for this order.")

    refund = RefundDB(
        order_id = order.id,
        amount = amount,
        status = "APPROVED"
    )

    db.add(refund)
    db.commit()
    db.refresh(refund)

    return RefundResponse(
        order_id = refund.order_id,
        amount = refund.amount,
        status = refund.status,
        message = "Refund approved successfully"
    )

def escalate_case(db: Session, order_id: str, reason: str, priority: str = 'HIGH') -> EscalationResponse:
    get_order_by_id(
        db = db,
        order_id = order_id
    )

    escalation = EscalationDB(
        order_id = order_id,
        reason = reason,
        priority = priority,
        status = "PENDING"
    )

    db.add(escalation)
    db.commit()
    db.refresh(escalation)

    return EscalationResponse(
        case_id = escalation.id,
        order_id = escalation.order_id,
        reason = escalation.reason,
        priority = escalation.priority,
        status = escalation.status
    )