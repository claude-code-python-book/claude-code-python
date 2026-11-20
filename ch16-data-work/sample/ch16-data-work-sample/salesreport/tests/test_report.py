import pandas as pd
import pytest

from salesreport.clean import clean_orders
from salesreport.report import money, summarize
from salesreport.validate import split_valid


@pytest.fixture
def summary(raw: pd.DataFrame):
    valid = split_valid(clean_orders(raw).orders, month="2026-10").valid
    return summarize(valid, "2026-10")


def test_only_completed_orders_count(summary) -> None:
    # ORD-1: 2 x 49.00, ORD-2: 1 x 1,249.00, ORD-8: 3 x 129.00
    assert summary.orders == 3
    assert summary.revenue_cents == 9800 + 124900 + 38700


def test_regions_are_sorted_by_revenue(summary) -> None:
    assert summary.by_region.to_dict("list") == {
        "region": ["East", "West", "North"],
        "orders": [1, 1, 1],
        "revenue_cents": [124900, 38700, 9800],
    }


def test_every_day_of_the_month_appears(summary) -> None:
    assert len(summary.daily) == 31
    assert summary.daily.loc["2026-10-02"] == 124900
    assert summary.daily.loc["2026-10-31"] == 0


@pytest.mark.parametrize(
    ("cents", "text"), [(0, "0.00"), (5, "0.05"), (123456789, "1,234,567.89")]
)
def test_money(cents: int, text: str) -> None:
    assert money(cents) == text
