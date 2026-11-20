"""The database constraints: the last line of defence. They need PostgreSQL."""

from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from bookings.models import Booking
from tests.django.factories import BookingFactory, tomorrow_at

pytestmark = pytest.mark.django_db


def test_the_database_refuses_a_double_booking() -> None:
    first = BookingFactory()
    with pytest.raises(IntegrityError), transaction.atomic():
        BookingFactory(room=first.room, start=first.start + timedelta(minutes=30))


def test_touching_bookings_are_allowed() -> None:
    first = BookingFactory()
    BookingFactory(room=first.room, start=first.end)  # starts as the first ends


def test_a_cancelled_booking_frees_its_slot() -> None:
    first = BookingFactory(status=Booking.Status.CANCELLED)
    BookingFactory(room=first.room, start=first.start)


def test_full_clean_reports_the_rules_and_the_overlap() -> None:
    first = BookingFactory()
    clash = Booking(
        room=first.room, user=first.user, start=tomorrow_at(7), end=first.end
    )
    with pytest.raises(ValidationError) as caught:
        clash.full_clean()
    messages = " ".join(caught.value.messages)
    assert "Rooms are open 08:00 to 20:00." in messages
    assert "This room is already booked at that time." in messages
