"""Command-line entry point for the monthly billing run."""

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from invoicer.billing import summarize_billing
from invoicer.csv_rows import read_rows

REQUIRED = ("invoice_id", "customer", "region", "sku", "qty", "unit_price", "issued")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="invoicer-billing",
        description="Bill every invoice in a CSV export from the billing system.",
    )
    parser.add_argument("export", type=Path, help="CSV export to bill")
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="billing date (default: today)",
    )
    parser.add_argument(
        "--report-dir", type=Path, metavar="DIR", help="also write DIR/customers.csv"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the billing; return 1 if any row was rejected, else 0."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        rows = read_rows(args.export, required=REQUIRED)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))  # prints usage and exits with status 2

    result = summarize_billing(rows, args.today, args.report_dir)
    for name, totals in sorted(result["customers"].items()):
        print(f"{name}: billed {totals['billed']}, outstanding {totals['outstanding']}")
    print(f"Grand total: {result['grand_total']}")
    for error in result["errors"]:
        print(error, file=sys.stderr)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
