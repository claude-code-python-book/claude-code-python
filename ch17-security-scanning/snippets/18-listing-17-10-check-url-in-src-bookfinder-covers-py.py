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
