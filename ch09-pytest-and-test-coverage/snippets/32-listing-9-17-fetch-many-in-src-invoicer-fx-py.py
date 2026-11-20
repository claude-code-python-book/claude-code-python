async def fetch_many(
    bases: Iterable[str], url: str = RATES_URL
) -> dict[str, dict[str, Decimal]]:
    """Fetch the rates for several base currencies concurrently."""
    codes = list(bases)
    tables = await asyncio.gather(
        *(asyncio.to_thread(fetch_rates, code, url) for code in codes)
    )
    return dict(zip(codes, tables, strict=True))
