"""manage.py purge_cancelled: delete old cancelled bookings."""

from datetime import timedelta
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from bookings.models import Booking


class Command(BaseCommand):
    """Delete cancelled bookings that ended more than --days days ago."""

    help = "Delete cancelled bookings that ended more than --days days ago."

    def add_arguments(self, parser: CommandParser) -> None:
        """Declare --days and --dry-run."""
        parser.add_argument("--days", type=int, default=90)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args: Any, days: int, dry_run: bool, **options: Any) -> None:
        """Count, then delete unless --dry-run."""
        cutoff = timezone.now() - timedelta(days=days)
        old = Booking.objects.filter(status=Booking.Status.CANCELLED, end__lt=cutoff)
        count = old.count()
        if not dry_run:
            old.delete()
        verb = "Would delete" if dry_run else "Deleted"
        self.stdout.write(self.style.SUCCESS(f"{verb} {count} cancelled bookings."))
