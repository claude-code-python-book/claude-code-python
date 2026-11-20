"""Messages to people, sent after the database change is committed."""

from django.core.mail import send_mail

from bookings.models import Booking


def send_booking_confirmation(booking_id: int) -> None:
    """Email the person who made the booking."""
    booking = Booking.objects.select_related("room", "user").get(pk=booking_id)
    send_mail(
        subject=f"Booked: {booking.room} on {booking.start:%d %b at %H:%M}",
        message=f"Your booking of {booking.room} is confirmed.",
        from_email=None,  # DEFAULT_FROM_EMAIL
        recipient_list=[booking.user.email],
    )
