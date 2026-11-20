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
