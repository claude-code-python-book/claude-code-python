def fetch_rates(base: str, url: str = RATES_URL) -> dict[str, Decimal]:
    """Return the rates from `base` to other currencies, as published at `url`."""
    if urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"rates URL must use http or https, not {url!r}")
    # The scheme is checked above, so urlopen can't be pointed at file: URLs.
    with urlopen(f"{url}?base={base}", timeout=5) as response:  # noqa: S310
        data = json.load(response, parse_float=Decimal)
    return {code: Decimal(rate) for code, rate in data["rates"].items()}
