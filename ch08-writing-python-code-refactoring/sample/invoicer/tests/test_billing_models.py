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
