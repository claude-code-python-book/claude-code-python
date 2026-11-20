"""Request and response models for the HTTP API."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .agent import ReviewReport


class ReviewRequest(BaseModel):
    repo: str = Field(min_length=1, max_length=64)
    base: str = Field(default="main", pattern=r"^[A-Za-z0-9._/][A-Za-z0-9._/-]{0,99}$")


class FindingOut(BaseModel):
    path: str
    line: int
    severity: str
    message: str


class ReviewResponse(BaseModel):
    findings: list[FindingOut]
    summary: str
    status: str
    cost_usd: float
    session_id: str

    @classmethod
    def from_report(cls, report: ReviewReport) -> ReviewResponse:
        return cls(
            findings=[FindingOut(**vars(f)) for f in report.findings],
            summary=report.summary, status=report.subtype,
            cost_usd=round(report.cost_usd, 4), session_id=report.session_id,
        )
