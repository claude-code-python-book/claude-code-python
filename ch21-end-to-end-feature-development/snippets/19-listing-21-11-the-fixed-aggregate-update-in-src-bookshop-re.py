# One UPDATE that adds in the database: no read-modify-write race.
row = self.session.execute(
    update(Book)
    .where(Book.id == book_id)
    .values(rating_count=Book.rating_count + 1,
            rating_total=Book.rating_total + stars)
    .returning(Book.rating_count, Book.rating_total)
).one()
return RatingSummary(row.rating_count, row.rating_total)
