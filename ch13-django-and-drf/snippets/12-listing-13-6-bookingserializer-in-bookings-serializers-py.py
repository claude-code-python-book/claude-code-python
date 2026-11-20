class BookingSerializer(serializers.ModelSerializer):
    """A booking. The user comes from the request, never from the body."""

    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.filter(is_active=True)
    )
    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "room", "room_name", "start", "end", "attendees", "status"]
        read_only_fields = ["status"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Check the booking rules, then whether the room is free."""
        room, start, end = attrs["room"], attrs["start"], attrs["end"]
        problems = rules.booking_problems(
            start,
            end,
            attrs.get("attendees", 1),
            room.capacity,
            timezone.now(),
            timezone.get_current_timezone(),
        )
        if problems:
            raise serializers.ValidationError(problems)
        clash = room.bookings.filter(
            status=Booking.Status.CONFIRMED, start__lt=end, end__gt=start
        )
        if clash.exists():
            raise serializers.ValidationError(
                "This room is already booked at that time."
            )
        return attrs
