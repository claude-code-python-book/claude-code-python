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
