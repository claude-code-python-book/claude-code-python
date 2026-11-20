"""SQLAlchemy implementations of the service's storage protocols."""

from __future__ import annotations

from types import TracebackType
from typing import Self

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from .models import Book, Review
from .ratings import RatingSummary
from .service import DuplicateReview, ReviewRepository


class SqlReviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def book_exists(self, book_id: int) -> bool:
        return self.session.get(Book, book_id) is not None

    def summary(self, book_id: int) -> RatingSummary:
        row = self.session.execute(
            select(Book.rating_count, Book.rating_total).where(Book.id == book_id)
        ).one()
        return RatingSummary(row.rating_count, row.rating_total)

    def add_review(self, book_id: int, user_id: str, stars: int,
                   comment: str) -> RatingSummary:
        self.session.add(Review(book_id=book_id, user_id=user_id,
                                stars=stars, comment=comment))
        try:
            self.session.flush()
        except IntegrityError as exc:
            raise DuplicateReview(f"{user_id} already reviewed {book_id}") from exc
        # One UPDATE that adds in the database: no read-modify-write race.
        row = self.session.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(rating_count=Book.rating_count + 1,
                    rating_total=Book.rating_total + stars)
            .returning(Book.rating_count, Book.rating_total)
        ).one()
        return RatingSummary(row.rating_count, row.rating_total)


class SqlUnitOfWork:
    session: Session
    reviews: ReviewRepository

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._factory = session_factory

    def __enter__(self) -> Self:
        self.session = self._factory()
        self.reviews = SqlReviewRepository(self.session)
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc: BaseException | None, tb: TracebackType | None) -> None:
        self.session.rollback()          # no-op after a successful commit
        self.session.close()

    def commit(self) -> None:
        self.session.commit()
