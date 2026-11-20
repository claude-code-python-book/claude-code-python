"""End to end over HTTP: MCP client -> broker -> tracker, as different people."""

import json

import anyio.to_thread
import httpx2
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from mcp.client import Client
from mcp.client.streamable_http import streamable_http_client

from acme_broker.register import register as register_token

from conftest import Env

pytestmark = pytest.mark.anyio


async def call(env: Env, token: str, tool: str, **args: object) -> tuple[bool, str]:
    """Call one tool as the holder of `token`; return (is_error, text)."""
    async with httpx2.AsyncClient(headers={"Authorization": f"Bearer {token}"},
                                  timeout=30) as http:
        transport = streamable_http_client(f"{env.url}/mcp", http_client=http)
        async with Client(transport) as c:
            result = await c.call_tool(tool, args)
    return result.is_error, result.content[0].text


async def register(env: Env, user: str, secret: str) -> int:
    return await anyio.to_thread.run_sync(
        lambda: register_token(env.url, env.mint(user), secret))


async def test_no_token_gets_401_pointing_at_metadata(env: Env) -> None:
    async with httpx2.AsyncClient() as http:
        r = await http.post(f"{env.url}/mcp", json={"jsonrpc": "2.0", "id": 1,
                                                     "method": "ping"},
                            headers={"accept": "application/json, text/event-stream"})
        meta = await http.get(f"{env.url}/.well-known/oauth-protected-resource/mcp")
    assert r.status_code == 401
    assert "resource_metadata=" in r.headers["www-authenticate"]
    assert meta.json()["authorization_servers"] == ["https://login.acme.example/"]


@pytest.mark.parametrize("bad", ["expired", "wrong-audience", "forged"])
async def test_bad_tokens_are_rejected(env: Env, bad: str) -> None:
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    token = {"expired": env.mint("alice@acme.example", ttl=-60),
             "wrong-audience": env.mint("alice@acme.example", aud="https://other/mcp"),
             "forged": env.mint("alice@acme.example", key=other)}[bad]
    async with httpx2.AsyncClient() as http:
        r = await http.post(f"{env.url}/mcp",
                            headers={"Authorization": f"Bearer {token}"},
                            json={"jsonrpc": "2.0", "id": 1, "method": "ping"})
    assert r.status_code == 401


async def test_each_developer_acts_as_themselves(env: Env) -> None:
    assert await register(env, "alice@acme.example", "trk-alice") == 200
    assert await register(env, "bob@acme.example", "trk-bob") == 200
    alice, bob = env.mint("alice@acme.example"), env.mint("bob@acme.example")

    err, text = await call(env, alice, "get_issue", key="PAY-142")
    assert not err and json.loads(text)["title"] == "Refunds over 10,000 INR fail"

    err, text = await call(env, bob, "get_issue", key="PAY-142")   # no PAY access
    assert err and "HTTP 403" in text

    err, text = await call(env, alice, "comment_on_issue", key="PAY-142",
                           body="On it")
    assert not err and json.loads(text)["author"] == "alice@acme.example"


async def test_scopes_and_missing_credentials(env: Env) -> None:
    reader = env.mint("alice@acme.example", scope="tracker:read")
    err, text = await call(env, reader, "comment_on_issue", key="PAY-142", body="x")
    assert err and "needs the tracker:write scope" in text

    carol = env.mint("carol@acme.example")
    err, text = await call(env, carol, "get_issue", key="WEB-7")
    assert err and "No tracker token registered" in text


async def test_revocation_cuts_every_connection(env: Env) -> None:
    await register(env, "dave@acme.example", "trk-bob")
    assert env.vault.revoke_user("dave@acme.example") == 1
    dave = env.mint("dave@acme.example")
    err, text = await call(env, dave, "get_issue", key="WEB-7")
    assert err and "No tracker token registered" in text


async def test_every_call_is_audited(env: Env) -> None:
    await register(env, "bob@acme.example", "trk-bob")
    await call(env, env.mint("bob@acme.example"), "get_issue", key="PAY-142")
    reader = env.mint("alice@acme.example", scope="tracker:read")
    await call(env, reader, "comment_on_issue", key="PAY-142", body="x")
    lines = [json.loads(x) for x in env.audit_path.read_text().splitlines()]
    outcomes = {(e["user"], e["tool"], e["outcome"]) for e in lines}
    assert ("bob@acme.example", "get_issue", "upstream_refused") in outcomes
    assert ("alice@acme.example", "comment_on_issue", "denied") in outcomes
    fields = {"ts", "user", "tool", "target", "outcome", "ms"}
    assert all(set(e) == fields for e in lines)
    assert not any("trk-" in json.dumps(e) for e in lines)      # no secrets logged


async def test_registration_needs_a_valid_identity(env: Env) -> None:
    async with httpx2.AsyncClient() as http:
        forged = await http.put(f"{env.url}/credentials/tracker",
                                json={"token": "x"},
                                headers={"Authorization": "Bearer not-a-jwt"})
        unknown = await http.put(f"{env.url}/credentials/payroll",
                                 json={"token": "x"},
                                 headers={"Authorization": f"Bearer {env.mint('a')}"})
    assert (forged.status_code, unknown.status_code) == (401, 404)
