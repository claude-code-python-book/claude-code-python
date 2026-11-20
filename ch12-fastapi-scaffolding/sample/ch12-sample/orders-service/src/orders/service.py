"""Business rules for orders. No FastAPI imports: HTTP stays in orders.api."""

from collections.abc import Callable
from datetime import UTC, datetime

from orders.domain import ALLOWED_MOVES, Line, Order, OrderStatus
from orders.errors import InvalidTransition, OrderNotFound
from orders.repository import OrderRepository
from orders.schemas import OrderCreate


def utc_now() -> datetime:
    """Return the current time in UTC."""
    return datetime.now(UTC)


class OrderService:
    """Place orders and move them through their statuses."""

    def __init__(
        self, repo: OrderRepository, clock: Callable[[], datetime] = utc_now
    ) -> None:
        self._repo = repo
        self._clock = clock

    def place(self, customer_id: str, data: OrderCreate) -> Order:
        """Create a pending order for the customer."""
        lines = [Line(x.sku, x.quantity, x.unit_price) for x in data.lines]
        return self._repo.add(customer_id, data.currency, lines, self._clock())

    def get(self, customer_id: str, order_id: int) -> Order:
        """Return the customer's order.

        Raises:
            OrderNotFound: If the order does not exist or belongs to another
                customer. Both cases look the same, so ids can't be probed.
        """
        order = self._repo.get(order_id)
        if order is None or order.customer_id != customer_id:
            raise OrderNotFound(order_id)
        return order

    def page(
        self, customer_id: str, status: OrderStatus | None, limit: int, offset: int
    ) -> tuple[list[Order], int]:
        """Return one page of the customer's orders and the total count."""
        return self._repo.page(customer_id, status, limit, offset)

    def pay(self, customer_id: str, order_id: int) -> Order:
        """Mark a pending order as paid."""
        return self._move(customer_id, order_id, OrderStatus.PAID)

    def cancel(self, customer_id: str, order_id: int) -> Order:
        """Cancel an order that has not shipped."""
        return self._move(customer_id, order_id, OrderStatus.CANCELLED)

    def _move(self, customer_id: str, order_id: int, target: OrderStatus) -> Order:
        order = self.get(customer_id, order_id)
        if target not in ALLOWED_MOVES[order.status]:
            raise InvalidTransition(order_id, order.status, target)
        order.status = target
        self._repo.save(order)
        return order
