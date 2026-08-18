from models import Order, OrderStatus, CancelOrderResponse
from exceptions import OrderNotFoundError, InvalidOrderActionError


def get_order_by_id(orders: dict[str, Order], order_id: str) -> Order:
    order = orders.get(order_id)

    if order is None:
        raise OrderNotFoundError(
            f"Order {order_id} not found"
        )

    return order


def cancel_order(orders: dict[str, Order], order_id: str) -> CancelOrderResponse:
    order = get_order_by_id(
        orders = orders,
        order_id = order_id,
    )

    if order.status != OrderStatus.PROCESSING:
        raise InvalidOrderActionError(
            f"Order cannot be cancelled while status is {order.status.value}"
        )

    order.status = OrderStatus.CANCELLED

    return CancelOrderResponse(
        order_id = order.id,
        status = order.status,
        message = "Order cancelled successfully",
    )