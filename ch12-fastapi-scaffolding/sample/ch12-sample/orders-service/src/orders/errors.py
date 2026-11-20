"""Errors the service raises. The API maps them to HTTP responses."""

from orders.domain import OrderStatus


class OrderError(Exception):
    """Base class for order errors a client can cause."""


class OrderNotFound(OrderError):
    """No order with this id belongs to the caller."""

    def __init__(self, order_id: int) -> None:
        super().__init__(f"Order {order_id} does not exist.")
        self.order_id = order_id


class InvalidTransition(OrderError):
    """The order's status does not allow the requested change."""

    def __init__(
        self, order_id: int, current: OrderStatus, target: OrderStatus
    ) -> None:
        super().__init__(f"Order {order_id} is {current} and cannot become {target}.")
        self.order_id = order_id
        self.current = current
        self.target = target
