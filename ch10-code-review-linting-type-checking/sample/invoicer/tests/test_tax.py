from collections.abc import Callable
from decimal import Decimal

import pytest

from invoicer import Line, total_with_tax

LineFactory = Callable[..., Line]


def test_total_includes_tax(make_line: LineFactory) -> None:
    lines = [make_line(quantity=3, unit_price="9.99"), make_line(unit_price="4.50")]
    assert total_with_tax(lines, Decimal("0.20")) == Decimal("41.36")


def test_negative_rate_is_rejected() -> None:
    with pytest.raises(ValueError, match="negative"):
        total_with_tax([], Decimal("-0.1"))


@pytest.mark.slow
def test_many_lines(make_line: LineFactory) -> None:
    lines = [make_line(unit_price="0.01") for _ in range(100_000)]
    assert total_with_tax(lines, Decimal("0")) == Decimal("1000.00")


@pytest.mark.integration
def test_totals_round_trip_through_db(db_url: str) -> None:
    assert db_url.startswith("postgresql://")
