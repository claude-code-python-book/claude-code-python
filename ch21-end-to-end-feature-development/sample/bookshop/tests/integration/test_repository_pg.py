"""SqlReviewRepository against a real PostgreSQL (CI's service container)."""

import os
from collections.abc import Iterator

import pytest

sqlalchemy = pytest.importorskip("sqlalchemy")
DATABASE_URL = os.environ.get("DATABASE_URL")
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not DATABASE_URL, reason="DATABASE_URL not set"),
]

from sqlalchemy.orm import Session, sessionmaker  # noqa: E402

from bookshop.models import Base, Book  # noqa: E402
from bookshop.repository import SqlReviewRepository, SqlUnitOfWork  # noqa: E402
from bookshop.service import DuplicateReview  # noqa: E402


@pytest.fixture
def factory() -> Iterator[sessionmaker[Session]]:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    make = sessionmaker(engine)
    with make.begin() as session:
        session.add(Book(id=1, title="Dune"))
    yield make
    engine.dispose()


def test_add_review_updates_aggregate(factory: sessionmaker[Session]) -> None:
    with SqlUnitOfWork(factory) as uow:
        assert uow.reviews.add_review(1, "ana", 5, "").total == 5
        summary = uow.reviews.add_review(1, "ben", 2, "")
        uow.commit()
    assert (summary.count, summary.total) == (2, 7)


def test_duplicate_review_is_rejected(factory: sessionmaker[Session]) -> None:
    with factory() as session:
        repo = SqlReviewRepository(session)
        repo.add_review(1, "ana", 5, "")
        with pytest.raises(DuplicateReview):
            repo.add_review(1, "ana", 4, "")
