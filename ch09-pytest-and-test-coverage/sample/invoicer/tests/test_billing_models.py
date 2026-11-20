from datetime import date

import pytest
from pydantic import ValidationError

from invoicer.billing_models import BillingRow

VALID = {
    "invoice_id": "INV-1",
    "customer": "Acme Ltd",
    "region": "UK",
    "sku": "WIDGET",
    "qty": "3",
    "unit_price": "9.99",
    "discount": "",
    "issued": "2026-10-01",
    "paid": "",
}


def test_blank_paid_means_unpaid() -> None:
    row = BillingRow.model_validate(VALID)
    assert row.paid is None
    assert row.issued == date(2026, 10, 1)


@pytest.mark.parametrize("qty", ["4.0", "two", "0"])
def test_rejects_bad_quantities(qty: str) -> None:
    with pytest.raises(ValidationError, match="qty"):
        BillingRow.model_validate({**VALID, "qty": qty})


def test_rejects_payment_before_issue() -> None:
    with pytest.raises(ValidationError, match="paid before issued"):
        BillingRow.model_validate({**VALID, "paid": "2026-09-30"})


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("unit_price", "NaN", "finite number"),
        ("unit_price", "Infinity", "finite number"),
        ("unit_price", "-0.01", "greater than or equal to 0"),
        ("customer", "   ", "at least 1 character"),
        ("region", "uk", "Input should be 'UK'"),
        ("qty", "1e2", "whole number"),
        ("issued", "2026-02-29", "YYYY-MM-DD"),
    ],
)
def test_rejects_invalid_values(field: str, value: str, message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        BillingRow.model_validate({**VALID, field: value})


@pytest.mark.parametrize(
    ("field", "value"), [("unit_price", "0"), ("issued", "2028-02-29")]
)
def test_accepts_boundary_values(field: str, value: str) -> None:
    row = BillingRow.model_validate({**VALID, field: value})
    assert str(getattr(row, field)) == value


def test_accepts_payment_on_the_day_of_issue() -> None:
    row = BillingRow.model_validate({**VALID, "paid": VALID["issued"]})
    assert row.paid == row.issued
