from decimal import Decimal

import pytest

from invoicer.tax import Line, total_with_tax


def test_total_includes_tax() -> None:
    lines = [Line("Widget", 3, Decimal("9.99")), Line("Cable", 1, Decimal("4.50"))]
    assert total_with_tax(lines, Decimal("0.20")) == Decimal("41.36")


def test_negative_rate_is_rejected() -> None:
    with pytest.raises(ValueError, match="negative"):
        total_with_tax([], Decimal("-0.1"))
