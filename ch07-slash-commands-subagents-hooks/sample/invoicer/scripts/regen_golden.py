"""Regenerate tests/golden/totals.json from the sample invoices below."""

import json
from decimal import Decimal
from pathlib import Path

from invoicer import Line, total_with_tax

SAMPLES = {
    "basic": ([Line("Widget", 3, Decimal("9.99"))], "0.20"),
    "zero_rate": ([Line("Cable", 2, Decimal("4.50"))], "0"),
}
GOLDEN = Path(__file__).resolve().parent.parent / "tests" / "golden" / "totals.json"


def main() -> None:
    totals = {
        name: str(total_with_tax(lines, Decimal(rate)))
        for name, (lines, rate) in SAMPLES.items()
    }
    GOLDEN.write_text(json.dumps(totals, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
