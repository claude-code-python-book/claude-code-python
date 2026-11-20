from datetime import date

import pytest

from invoicer.billing import summarize_billing
from invoicer.billing_run import run_billing

ROW = {
    "invoice_id": "INV-1",
    "customer": "Acme Ltd",
    "region": "UK",
    "sku": "WIDGET",
    "qty": "3",
    "unit_price": "9.99",
    "issued": "2026-11-01",
}
TODAY = date(2026, 11, 15)


def test_old_name_warns_and_gives_the_same_result() -> None:
    with pytest.warns(DeprecationWarning, match="summarize_billing"):
        result = run_billing([ROW], TODAY)
    assert result == summarize_billing([ROW], TODAY)
