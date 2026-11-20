class Booking(models.Model):
    """One person's booking of one room for a period of time."""

    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bookings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    attendees = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=10, choices=Status, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start"]
        indexes = [models.Index(fields=["user", "start"])]
        constraints = [
            models.CheckConstraint(
                condition=Q(end__gt=F("start")), name="booking_ends_after_start"
            ),
            ExclusionConstraint(
                name="no_double_booking",
                expressions=[
                    (
                        TsTzRange("start", "end", RangeBoundary()),
                        RangeOperators.OVERLAPS,
                    ),
                    ("room", RangeOperators.EQUAL),
                ],
                condition=Q(status="confirmed"),
                violation_error_message="This room is already booked at that time.",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.room} {self.start:%Y-%m-%d %H:%M}"

    def clean(self) -> None:
        """Apply the booking rules to new bookings (edits keep old bookings valid)."""
        if not self._state.adding or self.room_id is None:
            return
        problems = rules.booking_problems(
            self.start,
            self.end,
            self.attendees,
            self.room.capacity,
            timezone.now(),
            timezone.get_current_timezone(),
        )
        if problems:
            raise ValidationError(problems)
