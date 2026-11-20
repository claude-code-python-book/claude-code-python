def late_fee(gross: Decimal, days: int) -> Decimal:
    """Return the late fee on an overdue invoice.

    The fee is 1.5% of `gross` per period, capped at 10% of `gross`, rounded
    half-up to cents. Days 31 to 59 count as one period, days 60 to 89 as two,
    and so on: a new period starts every 30 days from day 60. Whether day 60
    should still be one period is an open question; see
    `docs/adr/0003-late-fee-periods.md`.

    Args:
        gross: The invoice total including tax.
        days: Days since the invoice was issued. Callers pass more than 30.

    Examples:
        >>> late_fee(Decimal("100.00"), 31)
        Decimal('1.50')
        >>> late_fee(Decimal("100.00"), 60)
        Decimal('3.00')
        >>> late_fee(Decimal("100.00"), 3650)
        Decimal('10.00')
    """
