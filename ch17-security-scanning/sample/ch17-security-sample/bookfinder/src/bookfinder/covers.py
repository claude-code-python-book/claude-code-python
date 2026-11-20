"""Download cover images from approved hosts only (SSRF protection)."""

import ipaddress
import socket
from collections.abc import Callable
from urllib.parse import urlsplit

import requests

ALLOWED_HOSTS = frozenset({"covers.openlibrary.org"})
MAX_BYTES = 2_000_000
Resolver = Callable[[str], list[str]]


class BlockedURLError(ValueError):
    """The URL is not one we are willing to fetch."""


def resolve(host: str) -> list[str]:
    """Return every address the host resolves to."""
    return sorted({str(info[4][0]) for info in socket.getaddrinfo(host, 443)})


def check_url(
    url: str, allowed: frozenset[str] = ALLOWED_HOSTS, resolver: Resolver = resolve
) -> str:
    """Return the URL if it is https, on the allowlist and resolves publicly."""
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise BlockedURLError(f"scheme not allowed: {parts.scheme!r}")
    host = (parts.hostname or "").lower()
    if host not in allowed:
        raise BlockedURLError(f"host not allowed: {host!r}")
    if parts.port not in (None, 443):
        raise BlockedURLError(f"port not allowed: {parts.port}")
    for address in resolver(host):
        if not ipaddress.ip_address(address).is_global:
            raise BlockedURLError(f"{host} resolves to non-public {address}")
    return url


def fetch_cover(url: str, session: requests.Session | None = None) -> bytes:
    """Fetch a cover image; redirects are refused, size and time are capped."""
    check_url(url)
    http = session or requests.Session()
    with http.get(url, timeout=5, allow_redirects=False, stream=True) as response:
        if response.is_redirect:
            raise BlockedURLError("redirects are not followed")
        response.raise_for_status()
        body: bytes = response.raw.read(MAX_BYTES + 1, decode_content=True)
    if len(body) > MAX_BYTES:
        raise BlockedURLError("cover image too large")
    return body
