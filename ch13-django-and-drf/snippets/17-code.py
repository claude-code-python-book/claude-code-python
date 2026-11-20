from bookings.models import Booking


def bookings_for_room(room_id: str):
    return Booking.objects.raw(f"SELECT * FROM bookings_booking WHERE room_id = {room_id}")


def busy_rooms(since: str):
    return Booking.objects.extra(where=[f"start >= '{since}'"])
