# Feature: star ratings (issue #42)

Readers can rate a book from 1 to 5 stars, once per book, with an optional
comment, and anyone can read a book's average rating.

## Acceptance criteria

1. `POST /books/{id}/reviews` with `{"stars": 1-5, "comment": "..."}` and the
   reader's identity returns 201 and the new rating summary.
2. A second review of the same book by the same reader returns 409; an unknown
   book returns 404; stars outside 1-5 or a comment over 2,000 characters, 422.
3. `GET /books/{id}/rating` returns `{"average": 4.33, "count": 3}`: the mean
   rounded half-up to two places, or `null` with no reviews.
4. When a review first takes a book with at least 5 reviews below an average
   of 2.50, the editors get one alert, not one per later review.
5. Concurrent reviews never lose an update.
