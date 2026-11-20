import os
from collections.abc import Callable
from decimal import Decimal

import pytest

from invoicer import Line


@pytest.fixture
def make_line() -> Callable[..., Line]:
    """Build a Line with sensible defaults; override only what the test cares about."""

    def _make(
        description: str = "Widget", quantity: int = 1, unit_price: str = "10.00"
    ) -> Line:
        return Line(description, quantity, Decimal(unit_price))

    return _make


@pytest.fixture
def db_url() -> str:
    """URL of the test database; skips the test when INVOICER_DB_URL is unset."""
    url = os.environ.get("INVOICER_DB_URL")
    if url is None:
        pytest.skip("INVOICER_DB_URL is not set")
    return url
