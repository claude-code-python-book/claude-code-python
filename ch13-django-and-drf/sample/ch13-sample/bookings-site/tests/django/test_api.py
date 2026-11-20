"""The bookings API, through DRF's APIClient. One test per status code."""

from datetime import timedelta

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from rest_framework.test import APIClient

from bookings.models import Booking
from tests.django.factories import BookingFactory, RoomFactory, UserFactory, tomorrow_at

pytestmark = pytest.mark.django_db


def body(room, hour=10, hours=1, attendees=2):
    start = tomorrow_at(hour)
    end = start + timedelta(hours=hours)
    return {
        "room": room.pk,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "attendees": attendees,
    }


def test_anonymous_requests_get_401() -> None:
    assert APIClient().get("/api/bookings/").status_code == 401


def test_create_returns_201_and_the_booking_belongs_to_the_caller(api, user) -> None:
    response = api.post("/api/bookings/", body(RoomFactory()), format="json")
    assert response.status_code == 201
    assert Booking.objects.get(pk=response.data["id"]).user == user


def test_the_confirmation_email_waits_for_the_commit(
    api, user, mailoutbox, django_capture_on_commit_callbacks
) -> None:
    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        api.post("/api/bookings/", body(RoomFactory(name="Ada")), format="json")
    assert len(callbacks) == 1
    assert [m.to for m in mailoutbox] == [[user.email]]
    assert mailoutbox[0].subject.startswith("Booked: Ada on ")


def test_broken_rules_are_a_400_with_every_message(api) -> None:
    response = api.post(
        "/api/bookings/",
        body(RoomFactory(capacity=2), hour=7, attendees=5),
        format="json",
    )
    assert response.status_code == 400
    assert len(response.data["non_field_errors"]) == 2


def test_a_taken_slot_is_a_400(api) -> None:
    taken = BookingFactory()
    response = api.post("/api/bookings/", body(taken.room), format="json")
    assert response.status_code == 400
    assert response.data["non_field_errors"] == [
        "This room is already booked at that time."
    ]


def test_users_only_see_their_own_bookings(api, user) -> None:
    mine = BookingFactory(user=user)
    BookingFactory()  # someone else's
    response = api.get("/api/bookings/")
    assert [b["id"] for b in response.data["results"]] == [mine.pk]


def test_someone_elses_booking_is_a_404(api) -> None:
    assert api.get(f"/api/bookings/{BookingFactory().pk}/").status_code == 404


def test_cancel_returns_200(api, user) -> None:
    booking = BookingFactory(user=user, start=timezone.now() + timedelta(days=2))
    response = api.post(f"/api/bookings/{booking.pk}/cancel/")
    assert (response.status_code, response.data["status"]) == (200, "cancelled")


def test_cancelling_inside_24_hours_is_a_409(api, user) -> None:
    soon = timezone.now() + timedelta(hours=2)
    booking = BookingFactory(user=user, start=soon)
    assert api.post(f"/api/bookings/{booking.pk}/cancel/").status_code == 409


def test_staff_can_cancel_late(api) -> None:
    staff = UserFactory(is_staff=True)
    api.force_authenticate(user=staff)
    booking = BookingFactory(start=timezone.now() + timedelta(hours=2))
    assert api.post(f"/api/bookings/{booking.pk}/cancel/").status_code == 200


def test_availability_lists_the_free_periods(api) -> None:
    taken = BookingFactory()  # tomorrow 10:00-11:00
    day = taken.start.date().isoformat()
    response = api.get(f"/api/rooms/{taken.room.pk}/availability/", {"date": day})
    assert response.status_code == 200
    assert [p["start"][11:16] for p in response.json()["free"]] == ["08:00", "11:00"]


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
