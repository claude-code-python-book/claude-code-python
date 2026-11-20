from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from loyalty.rules import (
    Entry,
    Tier,
    discount_for,
    points_for_order,
    points_to_expire,
    redemption_problems,
    tier_for,
)

T0 = datetime(2025, 1, 10, 12, 0, tzinfo=UTC)
YEAR = timedelta(days=365)


def d(value: str) -> Decimal:
    return Decimal(value)


@pytest.mark.parametrize(
    ("spend", "tier"),
    [
        ("0", Tier.BRONZE),
        ("499.99", Tier.BRONZE),
        ("500.00", Tier.SILVER),
        ("1999.99", Tier.SILVER),
        ("2000.00", Tier.GOLD),
    ],
)
def test_tier_thresholds_are_inclusive(spend: str, tier: Tier) -> None:
    assert tier_for(d(spend)) is tier


@pytest.mark.parametrize(
    ("total", "tier", "points"),
    [
        ("120.00", Tier.BRONZE, 120),
        ("120.99", Tier.BRONZE, 120),  # whole units only
        ("120.00", Tier.SILVER, 150),
        ("99.99", Tier.GOLD, 149),  # 149.985 rounds down
        ("0.99", Tier.BRONZE, 0),
    ],
)
def test_points_round_down(total: str, tier: Tier, points: int) -> None:
    assert points_for_order(d(total), tier) == points


def test_a_negative_total_is_a_bug() -> None:
    with pytest.raises(ValueError, match="negative"):
        points_for_order(d("-1.00"), Tier.BRONZE)


def test_points_are_worth_a_cent_each() -> None:
    assert discount_for(500) == d("5.00")
    assert discount_for(1234) == d("12.34")


def test_a_valid_redemption_has_no_problems() -> None:
    assert redemption_problems(500, balance=800, order_total=d("10.00")) == []


def test_every_broken_rule_is_reported() -> None:
    problems = redemption_problems(400, balance=300, order_total=d("6.00"))
    assert problems == [
        "Redeem at least 500 points.",
        "The balance is only 300 points.",
        "Points can pay for at most half of an order.",
    ]


def test_half_the_order_exactly_is_allowed() -> None:
    assert redemption_problems(1000, balance=1000, order_total=d("20.00")) == []
    assert redemption_problems(1001, balance=1001, order_total=d("20.00")) != []


def earn(points: int, at: datetime) -> Entry:
    return Entry("earn", points, at)


def redeem(points: int, at: datetime) -> Entry:
    return Entry("redeem", -points, at)


def test_nothing_expires_within_a_year() -> None:
    entries = [earn(300, T0)]
    assert points_to_expire(entries, T0 + YEAR - timedelta(seconds=1)) == 0


def test_points_expire_exactly_a_year_after_they_were_earned() -> None:
    assert points_to_expire([earn(300, T0)], T0 + YEAR) == 300


def test_redemptions_spend_the_oldest_points_first() -> None:
    entries = [
        earn(300, T0),
        earn(200, T0 + timedelta(days=200)),
        redeem(250, T0 + timedelta(days=300)),
    ]
    # 250 of the first 300 were spent, so only 50 are left to expire.
    assert points_to_expire(entries, T0 + YEAR) == 50
    # The second lot expires a year after it was earned.
    assert points_to_expire(entries, T0 + timedelta(days=200) + YEAR) == 250


def test_a_redemption_cant_use_points_that_already_expired() -> None:
    entries = [
        earn(300, T0),
        earn(200, T0 + timedelta(days=300)),
        redeem(150, T0 + timedelta(days=400)),  # the first lot is gone by then
    ]
    assert points_to_expire(entries, T0 + timedelta(days=400)) == 300


def test_points_already_written_off_are_not_counted_twice() -> None:
    entries = [
        earn(300, T0),
        Entry("expire", -300, T0 + YEAR),
        earn(100, T0 + YEAR + timedelta(days=1)),
    ]
    assert points_to_expire(entries, T0 + YEAR + timedelta(days=2)) == 0


def test_entries_are_read_in_time_order() -> None:
    late_first = [redeem(250, T0 + timedelta(days=300)), earn(300, T0)]
    assert points_to_expire(late_first, T0 + YEAR) == 50


def test_naive_times_are_refused() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        points_to_expire([earn(1, datetime(2025, 1, 1))], T0)
