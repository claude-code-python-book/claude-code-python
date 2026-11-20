def convert(amount: Decimal, base: str, target: str, url: str = RATES_URL) -> Decimal:
    """Convert an amount from one currency to another.

    Args:
        amount: The amount, in the `base` currency.
        base: The ISO 4217 code of `amount`'s currency, such as "GBP".
        target: The ISO 4217 code to convert to.
        url: The rates service to ask.

    Returns:
        The converted amount, rounded half-up to cents. If `base` and
        `target` are the same, `amount` is returned unchanged.

    Raises:
        ValueError: If the service publishes no rate from `base` to `target`.
    """
