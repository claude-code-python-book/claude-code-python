def convert(amount: Decimal, base: str, target: str, url: str = RATES_URL) -> Decimal:
    """Convert an amount from one currency to another.

    :param amount: The amount, in the ``base`` currency.
    :param base: The ISO 4217 code of the amount's currency, such as "GBP".
    :param target: The ISO 4217 code to convert to.
    :param url: The rates service to ask.
    :returns: The converted amount, rounded half-up to cents. If ``base`` and
        ``target`` are the same, ``amount`` is returned unchanged.
    :raises ValueError: If the service publishes no rate from ``base`` to
        ``target``.
    """
