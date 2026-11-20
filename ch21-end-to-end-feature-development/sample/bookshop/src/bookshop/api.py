"""FastAPI routes for reviews and ratings."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from .schemas import RatingOut, ReviewIn
from .service import BookNotFound, DuplicateReview, ReviewService

router = APIRouter(prefix="/books/{book_id}", tags=["ratings"])


def get_service(request: Request) -> ReviewService:
    service: ReviewService = request.app.state.review_service
    return service


def current_user(x_user_id: Annotated[str, Header(max_length=64)]) -> str:
    return x_user_id  # stand-in: a real app validates a session or token here


Service = Annotated[ReviewService, Depends(get_service)]
User = Annotated[str, Depends(current_user)]


@router.post("/reviews", status_code=status.HTTP_201_CREATED)
def create_review(book_id: int, body: ReviewIn, user: User,
                  service: Service) -> RatingOut:
    try:
        summary = service.add_review(book_id, user, body.stars, body.comment)
    except BookNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found") from None
    except DuplicateReview:
        raise HTTPException(status.HTTP_409_CONFLICT, "already reviewed") from None
    return RatingOut.from_summary(summary)


@router.get("/rating")
def get_rating(book_id: int, service: Service) -> RatingOut:
    try:
        return RatingOut.from_summary(service.rating(book_id))
    except BookNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "book not found") from None
