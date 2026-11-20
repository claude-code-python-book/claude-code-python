"""SSRF protection: only https URLs on the allowlist that resolve publicly."""

import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
import requests

from bookfinder.covers import BlockedURLError, check_url, fetch_cover

ALLOWED = frozenset({"covers.example.org"})


def public(host: str) -> list[str]:
    return ["93.184.215.14"]


@pytest.mark.parametrize(
    ("url", "reason"),
    [
        ("http://covers.example.org/a.jpg", "scheme"),
        ("https://169.254.169.254/latest/meta-data/", "host not allowed"),
        ("https://localhost/admin", "host not allowed"),
        ("https://2130706433/", "host not allowed"),  # 127.0.0.1 as one number
        ("https://covers.example.org.evil.test/a.jpg", "host not allowed"),
        ("https://covers.example.org@127.0.0.1/a.jpg", "host not allowed"),
        ("https://covers.example.org:8080/a.jpg", "port"),
    ],
)
def test_blocked_urls(url: str, reason: str) -> None:
    with pytest.raises(BlockedURLError, match=reason):
        check_url(url, ALLOWED, resolver=public)


@pytest.mark.parametrize("address", ["127.0.0.1", "10.0.0.7", "::1", "169.254.169.254"])
def test_allowed_host_resolving_to_internal_address_is_blocked(address: str) -> None:
    with pytest.raises(BlockedURLError, match="non-public"):
        check_url("https://covers.example.org/a.jpg", ALLOWED, lambda h: [address])


def test_allowed_public_url_passes() -> None:
    url = "https://covers.example.org/b/id/1-M.jpg"
    assert check_url(url, ALLOWED, resolver=public) == url


class _Redirect(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(302)
        self.send_header("Location", "http://127.0.0.1:1/admin")
        self.end_headers()

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def redirecting_server() -> Iterator[str]:
    server = HTTPServer(("127.0.0.1", 0), _Redirect)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/cover.jpg"
    server.shutdown()


def test_redirects_are_not_followed(
    redirecting_server: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Pretend the URL passed the allowlist, to test the next layer on its own.
    monkeypatch.setattr("bookfinder.covers.check_url", lambda url: url)
    with pytest.raises(BlockedURLError, match="redirects"):
        fetch_cover(redirecting_server, requests.Session())
