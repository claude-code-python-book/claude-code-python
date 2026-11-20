import pytest
from pydantic import ValidationError

from bookshop.ratings import RatingSummary
from bookshop.schemas import RatingOut, ReviewIn


@pytest.mark.parametrize("body", [
    {"stars": 0}, {"stars": 6}, {"stars": "5"}, {"stars": 4.5},
    {"stars": 5, "comment": "x" * 2001}, {"stars": 5, "user_id": "admin"},
])
def test_bad_review_bodies_are_rejected(body: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        ReviewIn.model_validate(body)


def test_rating_json() -> None:
    summary = RatingSummary(count=8, total=21)
    assert RatingOut.from_summary(summary).model_dump_json() == (
        '{"average":2.63,"count":8}')
    assert RatingOut.from_summary(RatingSummary()).model_dump_json() == (
        '{"average":null,"count":0}')
