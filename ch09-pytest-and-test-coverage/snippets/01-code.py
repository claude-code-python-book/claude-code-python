from datetime import date
from pathlib import Path

from invoicer.billing import summarize_billing
from invoicer.csv_rows import read_rows

SAMPLE = Path("tests/data/billing_sample.csv")


def test_billing() -> None:
    result = summarize_billing(read_rows(SAMPLE), date.today())
    assert result
    assert "grand_total" in result
