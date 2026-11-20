"""Pin what the billing run does today, before anyone refactors it.

These are characterization tests: the expected values are whatever the
code produced when the tests were written, not what a spec says. If a
change to them is intended, regenerate the golden files with
`uv run python scripts/regen_golden.py` and explain the diff in the PR.
"""

import json
from datetime import date
from pathlib import Path

from invoicer.billing import summarize_billing
from invoicer.csv_rows import read_rows

HERE = Path(__file__).parent
SAMPLE = HERE / "data" / "billing_sample.csv"
TODAY = date(2026, 11, 15)


def test_result_matches_golden() -> None:
    result = summarize_billing(read_rows(SAMPLE), TODAY)
    expected = json.loads((HERE / "golden" / "billing.json").read_text())
    assert result == expected


def test_report_matches_golden(tmp_path: Path) -> None:
    summarize_billing(read_rows(SAMPLE), TODAY, report_dir=tmp_path)
    report = (tmp_path / "customers.csv").read_text()
    assert report == (HERE / "golden" / "billing_customers.csv").read_text()
