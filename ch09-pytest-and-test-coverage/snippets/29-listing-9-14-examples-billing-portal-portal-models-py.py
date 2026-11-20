from datetime import date
from decimal import Decimal

from django.db import models
from invoicer.billing import late_fee


class Invoice(models.Model):
    number = models.CharField(max_length=20, unique=True)
    customer = models.CharField(max_length=100)
    gross = models.DecimalField(max_digits=12, decimal_places=2)
    issued = models.DateField()
    paid = models.DateField(null=True, blank=True)

    def fee_on(self, today: date) -> Decimal:
        """The late fee owed on `today`; nothing once paid or within 30 days."""
        days = (today - self.issued).days
        if self.paid is not None or days <= 30:
            return Decimal("0.00")
        return late_fee(self.gross, days)
