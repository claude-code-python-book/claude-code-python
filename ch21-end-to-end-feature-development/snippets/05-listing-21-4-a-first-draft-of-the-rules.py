def validate_stars(stars: int) -> int:
    assert 1 <= stars <= 5, "stars must be 1-5"
    return stars


@dataclass(frozen=True)
class RatingSummary:
    count: int = 0
    total: int = 0

    def add(self, stars: int) -> RatingSummary:
        return RatingSummary(self.count + 1, self.total + validate_stars(stars))

    @property
    def average(self) -> float:
        if self.count == 0:
            return None
        return round(self.total / self.count, 2)


def needs_alert(before: RatingSummary, after: RatingSummary) -> bool:
    return after.count >= ALERT_MIN_REVIEWS and after.average < ALERT_BELOW
