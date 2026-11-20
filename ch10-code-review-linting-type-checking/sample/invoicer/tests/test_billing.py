import csv
from collections.abc import Callable
from datetime import date
from pathlib import Path

import pytest

from invoicer.billing import summarize_billing

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
RowFactory = Callable[..., dict[str, str]]


def test_report_keeps_names_with_commas_in_one_column(tmp_path: Path) -> None:
    summarize_billing([{**ROW, "customer": "Smith, Jones & Co"}], TODAY, tmp_path)
    with (tmp_path / "customers.csv").open(newline="", encoding="utf-8") as f:
        records = list(csv.reader(f))
    assert records[1] == ["Smith, Jones & Co", "1", "35.96", "0.00", "35.96"]


def test_paid_invoice_owes_no_late_fee(make_row: RowFactory) -> None:
    row = make_row(issued="2026-01-01", paid="2026-03-01")
    result = summarize_billing([row], TODAY)
    assert result["invoices"]["INV-1"]["fee"] == "0.00"
    assert result["invoices"]["INV-1"]["status"] == "paid"


@pytest.mark.parametrize(
    ("issued", "status"),
    [("2026-10-16", "open"), ("2026-10-15", "overdue")],
    ids=["30-days-old", "31-days-old"],
)
def test_invoice_becomes_overdue_after_30_days(
    make_row: RowFactory, issued: str, status: str
) -> None:
    result = summarize_billing([make_row(issued=issued)], TODAY)
    assert result["invoices"]["INV-1"]["status"] == status


def test_rejects_an_invoice_whose_rows_disagree_on_region(make_row: RowFactory) -> None:
    rows = [make_row(), make_row(region="DE")]
    result = summarize_billing(rows, TODAY)
    assert result["errors"] == ["row 3: invoice INV-1 changes"]
