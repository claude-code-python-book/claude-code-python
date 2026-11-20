import csv
from datetime import date
from pathlib import Path

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


def test_report_keeps_names_with_commas_in_one_column(tmp_path: Path) -> None:
    summarize_billing([{**ROW, "customer": "Smith, Jones & Co"}], TODAY, tmp_path)
    with (tmp_path / "customers.csv").open(newline="", encoding="utf-8") as f:
        records = list(csv.reader(f))
    assert records[1] == ["Smith, Jones & Co", "1", "35.96", "0.00", "35.96"]
