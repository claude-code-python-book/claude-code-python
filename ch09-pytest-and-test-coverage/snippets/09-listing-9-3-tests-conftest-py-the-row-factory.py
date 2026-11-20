BASE_ROW = {
    "invoice_id": "INV-1",
    "customer": "Acme Ltd",
    "region": "UK",
    "sku": "WIDGET",
    "qty": "1",
    "unit_price": "100.00",
    "issued": "2026-10-01",
}


@pytest.fixture
def make_row() -> Callable[..., dict[str, str]]:
    """Build one valid export row; pass only the fields the test is about."""

    def _make(**fields: str) -> dict[str, str]:
        return {**BASE_ROW, **fields}

    return _make
