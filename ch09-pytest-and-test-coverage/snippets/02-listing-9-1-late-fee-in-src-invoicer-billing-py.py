def late_fee(gross: Decimal, days: int) -> Decimal:
    """1.5% of the gross per started 30 days past the first 30, capped at 10%."""
    periods = (days - 30) // 30 + 1
    fee = min(gross * Decimal("0.015") * periods, gross * Decimal("0.10"))
    return fee.quantize(CENT, rounding=ROUND_HALF_UP)
