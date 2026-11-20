def test_listing_bookings_costs_the_same_queries_for_1_or_20(api, user) -> None:
    def queries_for_list() -> int:
        with CaptureQueriesContext(connection) as ctx:
            assert api.get("/api/bookings/").status_code == 200
        return len(ctx.captured_queries)

    BookingFactory(user=user)
    one = queries_for_list()
    for hour in range(11, 19):
        BookingFactory(user=user, start=tomorrow_at(hour))
    assert queries_for_list() == one
