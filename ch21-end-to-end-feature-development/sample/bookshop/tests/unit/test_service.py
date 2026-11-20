import pytest

from bookshop.ratings import InvalidRating
from bookshop.service import BookNotFound, DuplicateReview, ReviewService

from fakes import MemoryRepo, MemoryUoW, RecordingQueue


def test_review_updates_the_summary(service: ReviewService) -> None:
    service.add_review(1, "ana", 5)
    summary = service.add_review(1, "ben", 4)
    assert (summary.count, summary.total) == (2, 9)
    assert service.rating(1) == summary


def test_alert_is_enqueued_after_the_commit(service: ReviewService,
                                            log: list[str]) -> None:
    for user, stars in [("a", 3), ("b", 3), ("c", 2), ("d", 2), ("e", 1)]:
        service.add_review(1, user, stars)
    assert log[-2:] == ["commit", "alert:1"]
    assert log.count("alert:1") == 1


def test_no_alert_when_the_commit_fails(repo: MemoryRepo, log: list[str]) -> None:
    for user, stars in [("a", 3), ("b", 3), ("c", 2), ("d", 2)]:
        repo.add_review(1, user, stars, "")
    failing = ReviewService(lambda: MemoryUoW(repo, log, fail_commit=True),
                            RecordingQueue(log))
    with pytest.raises(ConnectionError):
        failing.add_review(1, "e", 1)
    assert "alert:1" not in log
    assert log == ["rollback"]


def test_unknown_book(service: ReviewService) -> None:
    with pytest.raises(BookNotFound):
        service.add_review(99, "ana", 5)
    with pytest.raises(BookNotFound):
        service.rating(99)


def test_one_review_per_user_per_book(service: ReviewService) -> None:
    service.add_review(1, "ana", 5)
    with pytest.raises(DuplicateReview):
        service.add_review(1, "ana", 1)
    service.add_review(2, "ana", 1)               # another book is fine


@pytest.mark.parametrize("stars,comment", [(0, ""), (6, ""), (3, "x" * 2001)])
def test_invalid_input_never_reaches_storage(service: ReviewService,
                                             repo: MemoryRepo, stars: int,
                                             comment: str) -> None:
    with pytest.raises(ValueError):            # InvalidRating is a ValueError
        service.add_review(1, "ana", stars, comment)
    assert repo.summaries == {}


def test_invalid_rating_is_a_value_error() -> None:
    assert issubclass(InvalidRating, ValueError)
