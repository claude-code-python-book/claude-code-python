"""Regenerate the golden files in tests/golden/ from the current code."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from invoicer import Line, total_with_tax
from invoicer.billing import summarize_billing
from invoicer.csv_rows import read_rows

TESTS = Path(__file__).resolve().parent.parent / "tests"
GOLDEN = TESTS / "golden"
BILLING_SAMPLE = TESTS / "data" / "billing_sample.csv"
BILLING_TODAY = date(2026, 11, 15)  # must match test_billing_characterization.py

SAMPLES = {
    "basic": ([Line("Widget", 3, Decimal("9.99"))], "0.20"),
    "zero_rate": ([Line("Cable", 2, Decimal("4.50"))], "0"),
}


def write_json(name: str, data: object) -> None:
    (GOLDEN / name).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main() -> None:
    totals = {
        name: str(total_with_tax(lines, Decimal(rate)))
        for name, (lines, rate) in SAMPLES.items()
    }
    write_json("totals.json", totals)

    rows = read_rows(BILLING_SAMPLE)
    write_json("billing.json", summarize_billing(rows, BILLING_TODAY))
    with TemporaryDirectory() as tmp:
        summarize_billing(rows, BILLING_TODAY, report_dir=tmp)
        report = (Path(tmp) / "customers.csv").read_text()
    (GOLDEN / "billing_customers.csv").write_text(report)


if __name__ == "__main__":
    main()
