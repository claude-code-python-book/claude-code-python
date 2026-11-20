"""HTTP request and response bodies."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .ratings import RatingSummary
from .service import MAX_COMMENT


class ReviewIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stars: int = Field(ge=1, le=5, strict=True)
    comment: str = Field(default="", max_length=MAX_COMMENT)


class RatingOut(BaseModel):
    average: float | None
    count: int

    @classmethod
    def from_summary(cls, summary: RatingSummary) -> RatingOut:
        avg = summary.average
        return cls(average=None if avg is None else float(avg), count=summary.count)
