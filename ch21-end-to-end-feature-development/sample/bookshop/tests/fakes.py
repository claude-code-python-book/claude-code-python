"""In-memory stand-ins for the storage and queue protocols."""

from __future__ import annotations

from types import TracebackType
from typing import Self

from bookshop.ratings import RatingSummary
from bookshop.service import DuplicateReview


class MemoryRepo:
    def __init__(self, books: set[int]) -> None:
        self.books = books
        self.summaries: dict[int, RatingSummary] = {}
        self.reviewers: set[tuple[int, str]] = set()

    def book_exists(self, book_id: int) -> bool:
        return book_id in self.books

    def summary(self, book_id: int) -> RatingSummary:
        return self.summaries.get(book_id, RatingSummary())

    def add_review(self, book_id: int, user_id: str, stars: int,
                   comment: str) -> RatingSummary:
        if (book_id, user_id) in self.reviewers:
            raise DuplicateReview(user_id)
        self.reviewers.add((book_id, user_id))
        self.summaries[book_id] = self.summary(book_id).add(stars)
        return self.summaries[book_id]


class MemoryUoW:
    """Records commits in a shared event log, so tests can check ordering."""

    def __init__(self, repo: MemoryRepo, log: list[str], fail_commit: bool = False):
        self.reviews = repo
        self.log = log
        self.fail_commit = fail_commit

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc: BaseException | None, tb: TracebackType | None) -> None:
        if exc_type is not None:
            self.log.append("rollback")

    def commit(self) -> None:
        if self.fail_commit:
            raise ConnectionError("database went away")
        self.log.append("commit")


class RecordingQueue:
    def __init__(self, log: list[str]) -> None:
        self.log = log

    def low_rating_alert(self, book_id: int) -> None:
        self.log.append(f"alert:{book_id}")
