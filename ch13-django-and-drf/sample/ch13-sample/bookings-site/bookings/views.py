"""API views: thin, with the rules in bookings.rules."""

from datetime import datetime
from functools import partial

from django.db import IntegrityError, transaction
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from bookings import rules
from bookings.exceptions import Conflict
from bookings.models import Booking, Room
from bookings.notifications import send_booking_confirmation
from bookings.permissions import IsOwnerOrStaff
from bookings.serializers import (
    AvailabilityQuerySerializer,
    BookingSerializer,
    RoomSerializer,
)


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    """List and show rooms, and when they are free."""

    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer

    @action(detail=True, methods=["get"])
    def availability(self, request: Request, pk: str | None = None) -> Response:
        """Return the free periods of one room on ?date=YYYY-MM-DD."""
        room = self.get_object()
        query = AvailabilityQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        day = query.validated_data["date"]
        tz = timezone.get_current_timezone()
        opens = datetime.combine(day, rules.POLICY.opens, tzinfo=tz)
        closes = datetime.combine(day, rules.POLICY.closes, tzinfo=tz)
        taken = room.bookings.filter(
            status=Booking.Status.CONFIRMED, start__lt=closes, end__gt=opens
        ).values_list("start", "end")
        free = rules.free_slots(day, taken, tz)
        return Response(
            {
                "room": room.pk,
                "date": day,
                "free": [{"start": s, "end": e} for s, e in free],
            }
        )


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Create, list, show and cancel bookings. No edits: cancel and rebook."""

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self) -> QuerySet[Booking]:
        """Staff see every booking; everyone else sees only their own."""
        bookings = Booking.objects.select_related("room")
        if self.request.user.is_staff:
            return bookings
        return bookings.filter(user=self.request.user)

    def perform_create(self, serializer: BookingSerializer) -> None:
        """Save with the requesting user; the database settles races."""
        try:
            with transaction.atomic():
                booking = serializer.save(user=self.request.user)
        except IntegrityError as exc:  # another request took the slot first
            raise Conflict from exc
        transaction.on_commit(partial(send_booking_confirmation, booking.pk))

    @action(detail=True, methods=["post"])
    def cancel(self, request: Request, pk: str | None = None) -> Response:
        """Cancel a booking, up to 24 hours before it starts (staff: any time)."""
        booking = self.get_object()
        if booking.status == Booking.Status.CANCELLED:
            raise Conflict("This booking is already cancelled.")
        if not rules.can_cancel(booking.start, timezone.now(), request.user.is_staff):
            raise Conflict(
                "Bookings can be cancelled up to 24 hours before they start."
            )
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status"])
        return Response(self.get_serializer(booking).data)
