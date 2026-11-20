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
