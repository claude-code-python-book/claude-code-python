from collections.abc import Callable

import pytest

from orders.domain import OrderStatus
from orders.errors import InvalidTransition, OrderNotFound
from orders.repository import InMemoryOrderRepository
from orders.schemas import OrderCreate
from orders.service import OrderService
from tests.conftest import NOW

Make = Callable[..., OrderCreate]


def test_place_creates_a_pending_order_for_the_customer(
    service: OrderService, make_order: Make
) -> None:
    order = service.place("C-1001", make_order())
    assert (order.id, order.customer_id, order.status) == (
        1,
        "C-1001",
        OrderStatus.PENDING,
    )
    assert order.created_at == NOW


def test_another_customers_order_looks_like_a_missing_one(
    service: OrderService, make_order: Make
) -> None:
    order = service.place("C-1001", make_order())
    with pytest.raises(OrderNotFound) as other:
        service.get("C-2002", order.id)
    with pytest.raises(OrderNotFound) as missing:
        service.get("C-2002", 999)
    assert str(other.value) == f"Order {order.id} does not exist."
    assert type(other.value) is type(missing.value)


def test_a_paid_order_can_be_cancelled(service: OrderService, make_order: Make) -> None:
    order = service.place("C-1001", make_order())
    service.pay("C-1001", order.id)
    assert service.cancel("C-1001", order.id).status is OrderStatus.CANCELLED


@pytest.mark.parametrize("status", [OrderStatus.SHIPPED, OrderStatus.CANCELLED])
def test_a_finished_order_cannot_be_cancelled(
    service: OrderService,
    repo: InMemoryOrderRepository,
    make_order: Make,
    status: OrderStatus,
) -> None:
    order = service.place("C-1001", make_order())
    order.status = status
    repo.save(order)
    with pytest.raises(InvalidTransition, match=f"is {status} and cannot become"):
        service.cancel("C-1001", order.id)


def test_page_is_newest_first_and_filters_by_status(
    service: OrderService, make_order: Make
) -> None:
    first, second, third = (service.place("C-1001", make_order()) for _ in range(3))
    service.place("C-2002", make_order())
    service.pay("C-1001", second.id)

    orders, count = service.page("C-1001", None, limit=2, offset=0)
    assert [o.id for o in orders] == [third.id, second.id]
    assert count == 3
    paid, paid_count = service.page("C-1001", OrderStatus.PAID, limit=20, offset=0)
    assert [o.id for o in paid] == [second.id]
    assert paid_count == 1
