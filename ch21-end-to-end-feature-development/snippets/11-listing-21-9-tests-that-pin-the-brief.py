@pytest.mark.parametrize("stars,expected", [
    ((5, 4, 4), Decimal("4.33")),
    ((3, 3, 3, 3, 3, 2, 2, 2), Decimal("2.63")),   # 2.625 rounds half-up
    ((1, 2), Decimal("1.50")),
])
def test_average_rounds_half_up_to_two_places(stars: tuple[int, ...],
                                              expected: Decimal) -> None:
    assert summary_of(*stars).average == expected


def test_alert_does_not_repeat_while_average_stays_low() -> None:
    low = summary_of(3, 3, 2, 2, 1)
    assert not needs_alert(low, low.add(1))


def test_alert_is_enqueued_after_the_commit(service: ReviewService,
                                            log: list[str]) -> None:
    for user, stars in [("a", 3), ("b", 3), ("c", 2), ("d", 2), ("e", 1)]:
        service.add_review(1, user, stars)
    assert log[-2:] == ["commit", "alert:1"]
    assert log.count("alert:1") == 1
