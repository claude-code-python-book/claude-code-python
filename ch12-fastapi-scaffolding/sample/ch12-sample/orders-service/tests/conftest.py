from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import pytest

from orders.repository import InMemoryOrderRepository
from orders.schemas import OrderCreate
from orders.service import OrderService

NOW = datetime(2026, 11, 16, 9, 30, tzinfo=UTC)


@pytest.fixture
def repo() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def service(repo: InMemoryOrderRepository) -> OrderService:
    return OrderService(repo, clock=lambda: NOW)


@pytest.fixture
def make_order() -> Callable[..., OrderCreate]:
    """Build a valid OrderCreate; keyword arguments replace fields."""

    def make(**overrides: Any) -> OrderCreate:
        data: dict[str, Any] = {
            "currency": "GBP",
            "lines": [{"sku": "MUG-01", "quantity": 2, "unit_price": "4.50"}],
        }
        return OrderCreate.model_validate(data | overrides)

    return make
