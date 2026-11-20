"""Star ratings: the rules, with no I/O."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

MIN_STARS, MAX_STARS = 1, 5
ALERT_BELOW = Decimal("2.50")
ALERT_MIN_REVIEWS = 5


class InvalidRating(ValueError):
    pass


def validate_stars(stars: int) -> int:
    if isinstance(stars, bool) or not MIN_STARS <= stars <= MAX_STARS:
        raise InvalidRating(f"stars must be {MIN_STARS}-{MAX_STARS}, got {stars!r}")
    return stars


@dataclass(frozen=True)
class RatingSummary:
    count: int = 0
    total: int = 0

    def add(self, stars: int) -> RatingSummary:
        return RatingSummary(self.count + 1, self.total + validate_stars(stars))

    @property
    def average(self) -> Decimal | None:
        """Mean rating rounded half-up to 2 places; None with no reviews."""
        if self.count == 0:
            return None
        mean = Decimal(self.total) / Decimal(self.count)
        return mean.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def needs_alert(before: RatingSummary, after: RatingSummary) -> bool:
    """True only when this review pushes the average below the threshold."""
    if after.count < ALERT_MIN_REVIEWS or after.average is None:
        return False
    was_low = (before.count >= ALERT_MIN_REVIEWS and before.average is not None
               and before.average < ALERT_BELOW)
    return after.average < ALERT_BELOW and not was_low
