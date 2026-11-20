book = self.session.get_one(Book, book_id)
book.rating_count += 1
book.rating_total += stars
