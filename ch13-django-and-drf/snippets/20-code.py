transaction.on_commit(partial(send_booking_confirmation, booking.pk))
