from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from bookings.rules import Policy, booking_problems, can_cancel, free_slots, overlaps

LONDON = ZoneInfo("Europe/London")
NOW = datetime(2026, 11, 16, 9, 0, tzinfo=LONDON)


def at(day: int, hour: int, minute: int = 0, month: int = 11) -> datetime:
    return datetime(2026, month, day, hour, minute, tzinfo=LONDON)


def problems(
    start: datetime, end: datetime, attendees: int = 2, capacity: int = 8
) -> list[str]:
    return booking_problems(start, end, attendees, capacity, NOW, LONDON)


def test_a_normal_booking_has_no_problems() -> None:
    assert problems(at(18, 10), at(18, 11, 30)) == []


@pytest.mark.parametrize(
    ("start", "end", "message"),
    [
        (at(18, 10), at(18, 10, 15), "must last 30 to 240 minutes"),
        (at(18, 10), at(18, 15), "must last 30 to 240 minutes"),
        (at(18, 11), at(18, 10), "must last 30 to 240 minutes"),
        (at(16, 8), at(16, 9), "must start in the future"),
        (at(18, 10) + timedelta(days=91), at(18, 11) + timedelta(days=91), "90 days"),
        (at(18, 10, 5), at(18, 11, 5), "15-minute boundary"),
        (at(18, 7, 30), at(18, 9), "open 08:00 to 20:00"),
        (at(18, 19, 30), at(18, 20, 30), "open 08:00 to 20:00"),
    ],
)
def test_each_rule_reports_its_own_problem(
    start: datetime, end: datetime, message: str
) -> None:
    found = problems(start, end)
    assert any(message in p for p in found), found


def test_a_booking_may_end_exactly_at_closing_time() -> None:
    assert problems(at(18, 19), at(18, 20)) == []


def test_too_many_people_for_the_room() -> None:
    assert problems(at(18, 10), at(18, 11), attendees=9) == [
        "9 people is more than this room holds (8)."
    ]


def test_every_broken_rule_is_reported_at_once() -> None:
    assert len(problems(at(18, 7, 5), at(18, 7, 20), attendees=20)) == 4


def test_naive_datetimes_are_refused() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        booking_problems(datetime(2026, 11, 18, 10), at(18, 11), 1, 8, NOW, LONDON)


def test_length_is_real_time_across_a_clock_change() -> None:
    # Clocks go forward at 01:00 on 29 March 2026: 00:30-04:45 is 3h15m.
    night = Policy(opens=time(0), closes=time(23, 45))
    start, end = at(29, 0, 30, month=3), at(29, 4, 45, month=3)
    assert end - start == timedelta(hours=4, minutes=15)  # wall-clock arithmetic
    now = datetime(2026, 3, 1, tzinfo=UTC)
    assert booking_problems(start, end, 1, 8, now, LONDON, night) == []


@pytest.mark.parametrize(
    ("hours_before", "is_staff", "allowed"),
    [(24, False, True), (23.99, False, False), (1, True, True)],
)
def test_cancellation_closes_24_hours_before(
    hours_before: float, is_staff: bool, allowed: bool
) -> None:
    start = NOW + timedelta(hours=hours_before)
    assert can_cancel(start, NOW, is_staff) is allowed


def test_touching_periods_do_not_overlap() -> None:
    assert not overlaps((at(18, 10), at(18, 11)), (at(18, 11), at(18, 12)))
    assert overlaps((at(18, 10), at(18, 11)), (at(18, 10, 45), at(18, 12)))


def test_an_empty_day_is_free_from_opening_to_closing() -> None:
    assert free_slots(date(2026, 11, 18), [], LONDON) == [(at(18, 8), at(18, 20))]


def test_free_slots_skip_bookings_and_gaps_too_short_to_book() -> None:
    taken = [
        (at(18, 9), at(18, 10)),
        (at(18, 10, 15), at(18, 12)),  # leaves a 15-minute gap: not bookable
        (at(18, 19), at(18, 21)),  # runs past closing
    ]
    assert free_slots(date(2026, 11, 18), taken, LONDON) == [
        (at(18, 8), at(18, 9)),
        (at(18, 12), at(18, 19)),
    ]


def test_bookings_stored_in_utc_are_placed_on_the_local_day() -> None:
    # 10:00-11:00 in London in July is 09:00-10:00 UTC.
    taken = [
        (datetime(2026, 7, 1, 9, tzinfo=UTC), datetime(2026, 7, 1, 10, tzinfo=UTC))
    ]
    free = free_slots(date(2026, 7, 1), taken, LONDON)
    assert [(s.time(), e.time()) for s, e in free] == [
        (time(8), time(10)),
        (time(11), time(20)),
    ]
