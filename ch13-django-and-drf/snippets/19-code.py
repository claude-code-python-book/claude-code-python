@receiver(post_save, sender=Booking)
def email_on_booking(sender, instance, created, **kwargs):
    if created:
        send_booking_confirmation(instance.pk)
