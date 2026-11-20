"""Use cases for reviews. Talks to storage and the task queue via protocols."""

from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Protocol, Self

from .ratings import RatingSummary, needs_alert, validate_stars

MAX_COMMENT = 2000


class BookNotFound(LookupError):
    pass


class DuplicateReview(ValueError):
    pass


class ReviewRepository(Protocol):
    def book_exists(self, book_id: int) -> bool: ...
    def summary(self, book_id: int) -> RatingSummary: ...
    def add_review(self, book_id: int, user_id: str, stars: int,
                   comment: str) -> RatingSummary: ...


class UnitOfWork(Protocol):
    reviews: ReviewRepository

    def __enter__(self) -> Self: ...
    def __exit__(self, exc_type: type[BaseException] | None,
                 exc: BaseException | None, tb: TracebackType | None) -> None: ...
    def commit(self) -> None: ...


class TaskQueue(Protocol):
    def low_rating_alert(self, book_id: int) -> None: ...


class ReviewService:
    def __init__(self, uow: Callable[[], UnitOfWork], queue: TaskQueue) -> None:
        self._uow = uow
        self._queue = queue

    def add_review(self, book_id: int, user_id: str, stars: int,
                   comment: str = "") -> RatingSummary:
        validate_stars(stars)
        if len(comment) > MAX_COMMENT:
            raise ValueError(f"comment longer than {MAX_COMMENT} characters")
        with self._uow() as uow:
            if not uow.reviews.book_exists(book_id):
                raise BookNotFound(book_id)
            after = uow.reviews.add_review(book_id, user_id, stars, comment)
            uow.commit()
        # Derive "before" from the atomic result, not from an earlier read
        # that a concurrent review could make stale.
        before = RatingSummary(after.count - 1, after.total - stars)
        if needs_alert(before, after):
            self._queue.low_rating_alert(book_id)   # only after the commit
        return after

    def rating(self, book_id: int) -> RatingSummary:
        with self._uow() as uow:
            if not uow.reviews.book_exists(book_id):
                raise BookNotFound(book_id)
            return uow.reviews.summary(book_id)
