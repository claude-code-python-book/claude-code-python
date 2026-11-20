def test_the_database_refuses_a_double_booking() -> None:
    first = BookingFactory()
    with pytest.raises(IntegrityError), transaction.atomic():
        BookingFactory(room=first.room, start=first.start + timedelta(minutes=30))


def test_touching_bookings_are_allowed() -> None:
    first = BookingFactory()
    BookingFactory(room=first.room, start=first.end)  # starts as the first ends
