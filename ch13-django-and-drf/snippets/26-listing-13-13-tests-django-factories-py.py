"""Factory Boy factories: valid objects by default, override only what a test needs."""

from datetime import datetime, time, timedelta

import factory
from django.utils import timezone

from bookings.models import Booking, Room


def tomorrow_at(hour: int) -> datetime:
    """An aware datetime tomorrow at `hour`:00, in the current time zone."""
    day = timezone.localdate() + timedelta(days=1)
    return datetime.combine(day, time(hour), tzinfo=timezone.get_current_timezone())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda u: f"{u.username}@example.com")
    password = factory.django.Password("correct horse")


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.Sequence(lambda n: f"Room {n}")
    capacity = 8


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    room = factory.SubFactory(RoomFactory)
    user = factory.SubFactory(UserFactory)
    start = factory.LazyFunction(lambda: tomorrow_at(10))
    end = factory.LazyAttribute(lambda b: b.start + timedelta(hours=1))
    attendees = 2
