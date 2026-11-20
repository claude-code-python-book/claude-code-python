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
