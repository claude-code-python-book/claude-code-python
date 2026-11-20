"""SQLAlchemy 2.x models for books and reviews."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    rating_count: Mapped[int] = mapped_column(default=0, server_default="0")
    rating_total: Mapped[int] = mapped_column(default=0, server_default="0")


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("book_id", "user_id", name="uq_reviews_book_user"),
        CheckConstraint("stars BETWEEN 1 AND 5", name="ck_reviews_stars"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    user_id: Mapped[str] = mapped_column(String(64))
    stars: Mapped[int]
    comment: Mapped[str] = mapped_column(String(2000), default="")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
