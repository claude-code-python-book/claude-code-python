"""Run the tracker stub and the real broker on localhost, with a test IdP key."""

import socket
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import jwt
import pytest
import uvicorn
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa

from acme_broker.app import BrokerConfig, build_broker
from acme_broker.audit import AuditLog
from acme_broker.identity import IdpTokenVerifier
from acme_broker.vault import Vault

from tracker_stub import app as tracker_app

ISSUER = "https://login.acme.example"


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def serve(app: object, port: int) -> uvicorn.Server:
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                           log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    while not server.started:
        time.sleep(0.02)
    return server


@dataclass
class Env:
    url: str
    resource: str
    key: rsa.RSAPrivateKey
    vault: Vault
    audit_path: Path

    def mint(self, sub: str, scope: str = "tracker:read tracker:write", *,
             aud: str | None = None, ttl: int = 600, key: object = None) -> str:
        now = int(time.time())
        claims = {"iss": ISSUER, "sub": sub, "aud": aud or self.resource,
                  "scope": scope, "azp": "claude-code", "iat": now, "exp": now + ttl}
        return jwt.encode(claims, key or self.key, algorithm="RS256")


@pytest.fixture(scope="session")
def env(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Env]:
    tmp = tmp_path_factory.mktemp("broker")
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    t_port, b_port = free_port(), free_port()
    resource = f"http://127.0.0.1:{b_port}/mcp"
    vault = Vault(tmp / "vault.json", Fernet.generate_key())
    audit = tmp / "audit.jsonl"
    cfg = BrokerConfig(
        issuer=ISSUER, resource_url=resource,
        verifier=IdpTokenVerifier(ISSUER, resource, lambda _t: key.public_key()),
        vault=vault, audit=AuditLog(audit), tracker_url=f"http://127.0.0.1:{t_port}",
        allowed_hosts=[f"127.0.0.1:{b_port}"])
    servers = [serve(tracker_app, t_port), serve(build_broker(cfg), b_port)]
    yield Env(f"http://127.0.0.1:{b_port}", resource, key, vault, audit)
    for s in servers:
        s.should_exit = True


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
