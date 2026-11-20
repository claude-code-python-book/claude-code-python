def points_for_order(
    total: Decimal, tier: Tier, programme: Programme = PROGRAMME
) -> int:
    """Return the points an order earns: one per whole unit, times the tier rate.

    Raises:
        ValueError: If the total is negative.
    """
    if total < 0:
        raise ValueError("An order total can't be negative.")
    rate = {
        Tier.BRONZE: Decimal(1),
        Tier.SILVER: programme.silver_rate,
        Tier.GOLD: programme.gold_rate,
    }[tier]
    return int((total * rate).to_integral_value(rounding=ROUND_FLOOR))
