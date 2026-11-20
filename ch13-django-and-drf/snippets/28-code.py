def test_users_only_see_their_own_bookings(api, user) -> None:
    mine = BookingFactory(user=user)
    BookingFactory()  # someone else's
    response = api.get("/api/bookings/")
    assert [b["id"] for b in response.data["results"]] == [mine.pk]


def test_someone_elses_booking_is_a_404(api) -> None:
    assert api.get(f"/api/bookings/{BookingFactory().pk}/").status_code == 404
