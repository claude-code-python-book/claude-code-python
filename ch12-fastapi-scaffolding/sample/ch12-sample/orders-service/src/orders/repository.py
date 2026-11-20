"""Order storage. The service depends on the protocol, not on a database."""

import threading
from collections.abc import Sequence
from datetime import datetime
from itertools import count
from typing import Protocol

from orders.domain import Line, Order, OrderStatus


class OrderRepository(Protocol):
    """What the service needs from order storage."""

    def add(
        self,
        customer_id: str,
        currency: str,
        lines: Sequence[Line],
        created_at: datetime,
    ) -> Order:
        """Store a new order and return it with its id."""
        ...

    def get(self, order_id: int) -> Order | None:
        """Return the order, or None if there is no such id."""
        ...

    def page(
        self, customer_id: str, status: OrderStatus | None, limit: int, offset: int
    ) -> tuple[list[Order], int]:
        """Return one page of a customer's orders, newest first, and the count."""
        ...

    def save(self, order: Order) -> None:
        """Store changes to an existing order."""
        ...


class InMemoryOrderRepository:
    """A thread-safe repository for tests and local development."""

    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._ids = count(1)
        self._lock = threading.Lock()

    def add(
        self,
        customer_id: str,
        currency: str,
        lines: Sequence[Line],
        created_at: datetime,
    ) -> Order:
        """Store a new order and return it with its id."""
        with self._lock:
            order = Order(
                next(self._ids), customer_id, currency, list(lines), created_at
            )
            self._orders[order.id] = order
        return order

    def get(self, order_id: int) -> Order | None:
        """Return the order, or None if there is no such id."""
        return self._orders.get(order_id)

    def page(
        self, customer_id: str, status: OrderStatus | None, limit: int, offset: int
    ) -> tuple[list[Order], int]:
        """Return one page of a customer's orders, newest first, and the count."""
        with self._lock:
            mine = [
                o
                for o in reversed(self._orders.values())
                if o.customer_id == customer_id and status in (None, o.status)
            ]
        return mine[offset : offset + limit], len(mine)

    def save(self, order: Order) -> None:
        """Store changes to an existing order."""
        with self._lock:
            self._orders[order.id] = order
