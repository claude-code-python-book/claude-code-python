from decimal import Decimal

import pytest

from bookshop.ratings import InvalidRating, RatingSummary, needs_alert, validate_stars


def summary_of(*stars: int) -> RatingSummary:
    s = RatingSummary()
    for n in stars:
        s = s.add(n)
    return s


@pytest.mark.parametrize("bad", [0, 6, -1, True])
def test_stars_outside_1_to_5_are_rejected(bad: int) -> None:
    with pytest.raises(InvalidRating):
        validate_stars(bad)


def test_no_reviews_has_no_average() -> None:
    assert RatingSummary().average is None


@pytest.mark.parametrize("stars,expected", [
    ((5, 4, 4), Decimal("4.33")),
    ((3, 3, 3, 3, 3, 2, 2, 2), Decimal("2.63")),   # 2.625 rounds half-up
    ((1, 2), Decimal("1.50")),
])
def test_average_rounds_half_up_to_two_places(stars: tuple[int, ...],
                                              expected: Decimal) -> None:
    assert summary_of(*stars).average == expected


def test_alert_fires_when_average_first_drops_below_threshold() -> None:
    before = summary_of(3, 3, 2, 2)                 # only 4 reviews
    assert needs_alert(before, before.add(1))       # 5 reviews, average 2.20


def test_alert_does_not_repeat_while_average_stays_low() -> None:
    low = summary_of(3, 3, 2, 2, 1)
    assert not needs_alert(low, low.add(1))


def test_no_alert_below_minimum_review_count() -> None:
    assert not needs_alert(summary_of(1), summary_of(1, 1))
