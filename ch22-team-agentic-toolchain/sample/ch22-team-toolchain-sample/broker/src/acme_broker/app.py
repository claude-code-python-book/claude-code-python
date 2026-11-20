"""The credential broker: one remote MCP server in front of the issue tracker.

Developers authenticate to the broker with their company identity. The broker
calls the tracker with that developer's own tracker token, which it keeps
encrypted and never sends to the developer's machine.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Any

import httpx2
from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.settings import AuthSettings
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import AnyHttpUrl
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

from .audit import AuditLog
from .identity import IdpTokenVerifier
from .vault import Vault

READ, WRITE = "tracker:read", "tracker:write"


@dataclass
class BrokerConfig:
    issuer: str                 # the company identity provider
    resource_url: str           # this broker's MCP endpoint, e.g. https://mcp.acme.example/mcp
    verifier: IdpTokenVerifier
    vault: Vault
    audit: AuditLog
    tracker_url: str
    allowed_hosts: list[str]


def build_broker(cfg: BrokerConfig) -> Starlette:
    mcp = MCPServer(
        "acme-tracker",
        instructions="Read and comment on Acme tracker issues as the signed-in user.",
        token_verifier=cfg.verifier,
        auth=AuthSettings(issuer_url=AnyHttpUrl(cfg.issuer),
                          resource_server_url=AnyHttpUrl(cfg.resource_url),
                          required_scopes=[READ],
                          validate_token_resource=True),
    )

    @asynccontextmanager
    async def guard(tool: str, scope: str, target: str) -> AsyncIterator[str]:
        """Check scope, fetch this user's tracker token, audit the outcome."""
        token = get_access_token()
        user = token.subject if token and token.subject else "anonymous"
        started, outcome = perf_counter(), "error"
        try:
            if token is None or scope not in token.scopes:
                outcome = "denied"
                raise ToolError(f"{tool} needs the {scope} scope")
            secret = cfg.vault.get(user, "tracker")
            if secret is None:
                outcome = "no_credential"
                raise ToolError("No tracker token registered for you; "
                                "run python -m acme_broker.register once")
            yield secret
            outcome = "ok"
        except ToolError:
            if outcome == "error":
                outcome = "upstream_refused"
            raise
        finally:
            cfg.audit.record(user, tool, target, outcome, started)

    async def tracker(method: str, path: str, secret: str, *, body: Any = None,
                      params: dict[str, Any] | None = None) -> Any:
        async with httpx2.AsyncClient(base_url=cfg.tracker_url, timeout=10) as http:
            resp = await http.request(method, path, json=body, params=params,
                                      headers={"Authorization": f"Bearer {secret}"})
        if resp.status_code in (401, 403, 404):
            raise ToolError(f"Tracker refused {method} {path}: HTTP {resp.status_code}")
        resp.raise_for_status()
        return resp.json()

    @mcp.tool()
    async def get_issue(key: str) -> dict[str, Any]:
        """Fetch one issue, such as PAY-142, with its description and status."""
        async with guard("get_issue", READ, key) as secret:
            return dict(await tracker("GET", f"/api/issues/{key}", secret))

    @mcp.tool()
    async def search_issues(query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search issues you can see by text; returns key, title and status."""
        async with guard("search_issues", READ, query) as secret:
            hits = await tracker("GET", "/api/issues", secret,
                                 params={"q": query, "limit": min(limit, 20)})
            return list(hits)

    @mcp.tool()
    async def comment_on_issue(key: str, body: str) -> dict[str, Any]:
        """Add a comment to an issue, posted as you."""
        async with guard("comment_on_issue", WRITE, key) as secret:
            return dict(await tracker("POST", f"/api/issues/{key}/comments", secret,
                                      body={"body": body[:4000]}))

    async def register(request: Request) -> JSONResponse:
        """A developer stores their own upstream token. Bearer-authenticated."""
        auth = request.headers.get("authorization", "")
        token = await cfg.verifier.verify_token(auth.removeprefix("Bearer "))
        if token is None or token.subject is None:
            return JSONResponse({"error": "invalid_token"}, status_code=401)
        system = request.path_params["system"]
        if system != "tracker":
            return JSONResponse({"error": "unknown system"}, status_code=404)
        secret = (await request.json()).get("token", "")
        if not secret:
            return JSONResponse({"error": "token required"}, status_code=422)
        cfg.vault.put(token.subject, system, secret)
        return JSONResponse({"stored": system, "for": token.subject})

    mcp.custom_route("/credentials/{system}", methods=["PUT"])(register)

    return mcp.streamable_http_app(transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True, allowed_hosts=cfg.allowed_hosts))
