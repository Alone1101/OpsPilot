from sqlalchemy.orm import Session
from models import OrderStatus, CancelOrderResponse
from db_models import OrderDB
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