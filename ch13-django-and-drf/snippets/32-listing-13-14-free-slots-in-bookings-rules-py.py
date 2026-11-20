def free_slots(
    day: date,
    taken: Iterable[tuple[datetime, datetime]],
    tz: tzinfo,
    policy: Policy = POLICY,
) -> list[tuple[datetime, datetime]]:
    """Return the free periods on `day`, in `tz`, long enough to book."""
    opens = datetime.combine(day, policy.opens, tzinfo=tz).astimezone(UTC)
    closes = datetime.combine(day, policy.closes, tzinfo=tz).astimezone(UTC)
    free: list[tuple[datetime, datetime]] = []
    cursor = opens
    for start, end in sorted((s.astimezone(UTC), e.astimezone(UTC)) for s, e in taken):
        if end <= cursor or start >= closes:
            continue
        if start - cursor >= policy.shortest:
            free.append((cursor, start))
        cursor = max(cursor, end)
    if closes - cursor >= policy.shortest:
        free.append((cursor, closes))
    return [(s.astimezone(tz), e.astimezone(tz)) for s, e in free]
