import json
import os
import threading
from collections.abc import Callable, Iterator
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

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


RATES = {
    "GBP": {"EUR": 1.15, "USD": 1.27},
    "EUR": {"GBP": 0.87, "USD": 1.10},
}


class RatesHandler(BaseHTTPRequestHandler):
    """Serves RATES the way the real rates service does: /latest?base=GBP."""

    def do_GET(self) -> None:
        base = parse_qs(urlsplit(self.path).query).get("base", [""])[0]
        if base not in RATES:
            self.send_error(404)
            return
        body = json.dumps({"base": base, "rates": RATES[base]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass  # keep pytest's output clean


@pytest.fixture(scope="session")
def rates_server() -> Iterator[str]:
    """A local rates service on a free port, started once per test session."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), RatesHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/latest"
    server.shutdown()
    server.server_close()
