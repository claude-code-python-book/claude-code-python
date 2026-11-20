@dataclass(frozen=True)
class Policy:
    """The booking policy. One place to change it, one place to test it."""

    opens: time = time(8)
    closes: time = time(20)
    slot: timedelta = timedelta(minutes=15)
    shortest: timedelta = timedelta(minutes=30)
    longest: timedelta = timedelta(hours=4)
    book_ahead: timedelta = timedelta(days=90)
    cancel_before: timedelta = timedelta(hours=24)


POLICY = Policy()


def _minutes(span: timedelta) -> int:
    return int(span.total_seconds() // 60)


def _on_slot(moment: datetime, policy: Policy) -> bool:
    since_midnight = timedelta(hours=moment.hour, minutes=moment.minute)
    return moment.second == moment.microsecond == 0 and not since_midnight % policy.slot


def booking_problems(
    start: datetime,
    end: datetime,
    attendees: int,
    capacity: int,
    now: datetime,
    tz: tzinfo,
    policy: Policy = POLICY,
) -> list[str]:
    """Return every rule a booking breaks; an empty list means it is allowed.

    Durations are measured in UTC. Python ignores the UTC offset when it
    subtracts two datetimes that share a tzinfo, so a local-time subtraction
    across a daylight-saving change would be off by an hour.

    Raises:
        ValueError: If start or end has no time zone.
    """
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("start and end must be timezone-aware")
    problems: list[str] = []
    length = end.astimezone(UTC) - start.astimezone(UTC)
    if not policy.shortest <= length <= policy.longest:
        problems.append(
            f"A booking must last {_minutes(policy.shortest)} to "
            f"{_minutes(policy.longest)} minutes."
        )
    if start <= now:
        problems.append("A booking must start in the future.")
    elif start - now > policy.book_ahead:
        problems.append(f"Bookings open {policy.book_ahead.days} days ahead.")
    local_start, local_end = start.astimezone(tz), end.astimezone(tz)
    if not (_on_slot(local_start, policy) and _on_slot(local_end, policy)):
        problems.append(
            f"Start and end must be on a {_minutes(policy.slot)}-minute boundary."
        )
    if (
        local_start.date() != local_end.date()
        or local_start.time() < policy.opens
        or local_end.time() > policy.closes
    ):
        problems.append(
            f"Rooms are open {policy.opens:%H:%M} to {policy.closes:%H:%M}."
        )
    if attendees > capacity:
        problems.append(
            f"{attendees} people is more than this room holds ({capacity})."
        )
    return problems
