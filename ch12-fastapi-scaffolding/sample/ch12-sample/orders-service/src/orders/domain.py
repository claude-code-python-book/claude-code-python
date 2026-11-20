"""The order model the service works with, independent of HTTP."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class OrderStatus(StrEnum):
    """Where an order is in its life."""

    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


ALLOWED_MOVES: dict[OrderStatus, frozenset[OrderStatus]] = {
    OrderStatus.PENDING: frozenset({OrderStatus.PAID, OrderStatus.CANCELLED}),
    OrderStatus.PAID: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
    OrderStatus.SHIPPED: frozenset(),
    OrderStatus.CANCELLED: frozenset(),
}


@dataclass
class Line:
    """One product on an order."""

    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class Order:
    """An order as the service and the repository see it."""

    id: int
    customer_id: str
    currency: str
    lines: list[Line]
    created_at: datetime
    status: OrderStatus = field(default=OrderStatus.PENDING)
