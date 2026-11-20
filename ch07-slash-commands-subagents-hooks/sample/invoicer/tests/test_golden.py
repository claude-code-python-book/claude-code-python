import json
from decimal import Decimal
from pathlib import Path

from invoicer import Line, total_with_tax

GOLDEN = json.loads((Path(__file__).parent / "golden" / "totals.json").read_text())


def test_basic_total_matches_golden() -> None:
    lines = [Line("Widget", 3, Decimal("9.99"))]
    assert str(total_with_tax(lines, Decimal("0.20"))) == GOLDEN["basic"]
