def test_the_confirmation_email_waits_for_the_commit(
    api, user, mailoutbox, django_capture_on_commit_callbacks
) -> None:
    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        api.post("/api/bookings/", body(RoomFactory(name="Ada")), format="json")
    assert len(callbacks) == 1
    assert [m.to for m in mailoutbox] == [[user.email]]
    assert mailoutbox[0].subject.startswith("Booked: Ada on ")
