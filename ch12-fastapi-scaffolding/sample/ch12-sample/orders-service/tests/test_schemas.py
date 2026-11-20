import json
from collections.abc import Callable
from decimal import Decimal

import pytest
from pydantic import ValidationError

from orders.domain import Line, Order
from orders.schemas import OrderCreate, OrderRead
from tests.conftest import NOW

MUG = {"sku": "MUG-01", "quantity": 1, "unit_price": "4.50"}


def test_valid_order_parses_prices_as_decimal(
    make_order: Callable[..., OrderCreate],
) -> None:
    assert make_order().lines[0].unit_price == Decimal("4.50")


def test_the_same_sku_twice_is_rejected(make_order: Callable[..., OrderCreate]) -> None:
    with pytest.raises(ValidationError, match="each SKU may appear once"):
        make_order(lines=[MUG, MUG])


def test_a_client_cannot_choose_the_customer(
    make_order: Callable[..., OrderCreate],
) -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        make_order(customer_id="C-9999")


@pytest.mark.parametrize(
    ("field", "value"),
    [("quantity", 0), ("quantity", 101), ("unit_price", "4.505"), ("sku", "mug 1")],
)
def test_bad_line_values_are_rejected(
    make_order: Callable[..., OrderCreate], field: str, value: object
) -> None:
    with pytest.raises(ValidationError):
        make_order(lines=[MUG | {field: value}])


def test_order_read_computes_total_and_keeps_money_as_strings() -> None:
    order = Order(7, "C-1001", "GBP", [Line("MUG-01", 3, Decimal("4.50"))], NOW)
    body = json.loads(OrderRead.model_validate(order).model_dump_json())
    assert body["total"] == "13.50"
    assert body["lines"][0]["unit_price"] == "4.50"
    assert body["status"] == "pending"


def test_total_is_read_only_in_the_response_schema() -> None:
    schema = OrderRead.model_json_schema(mode="serialization")
    assert schema["properties"]["total"]["readOnly"] is True
    assert "total" in schema["required"]
