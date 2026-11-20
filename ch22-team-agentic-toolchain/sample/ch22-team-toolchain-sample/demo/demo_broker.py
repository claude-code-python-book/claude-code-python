"""Run the tracker stub and the broker on localhost for the CLI demos.

Writes a developer token for alice (signed by a throwaway test IdP key) and
registers her tracker token, then serves until killed.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "broker"
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]

import jwt  # noqa: E402
import uvicorn  # noqa: E402
from conftest import serve  # noqa: E402
from starlette.applications import Starlette  # noqa: E402
from starlette.responses import JSONResponse  # noqa: E402
from starlette.routing import Route  # noqa: E402
from cryptography.fernet import Fernet  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import rsa  # noqa: E402
from tracker_stub import app as tracker_app  # noqa: E402

from acme_broker.app import BrokerConfig, build_broker  # noqa: E402
from acme_broker.audit import AuditLog  # noqa: E402
from acme_broker.identity import IdpTokenVerifier  # noqa: E402
from acme_broker.vault import Vault  # noqa: E402

ISSUER = "http://127.0.0.1:8773"   # a local stand-in for the company IdP
idp = Starlette(routes=[Route("/.well-known/oauth-authorization-server",
    lambda _r: JSONResponse({
        "issuer": ISSUER, "authorization_endpoint": f"{ISSUER}/authorize",
        "token_endpoint": f"{ISSUER}/token", "registration_endpoint": f"{ISSUER}/register",
        "response_types_supported": ["code"], "code_challenge_methods_supported": ["S256"],
        "grant_types_supported": ["authorization_code", "refresh_token"]}))])
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
resource = "http://127.0.0.1:8772/mcp"
vault = Vault(out / "vault.json", Fernet.generate_key())
vault.put("alice@acme.example", "tracker", "trk-alice")
cfg = BrokerConfig(issuer=ISSUER, resource_url=resource,
                   verifier=IdpTokenVerifier(ISSUER, resource, lambda _t: key.public_key()),
                   vault=vault, audit=AuditLog(out / "audit.jsonl"),
                   tracker_url="http://127.0.0.1:8771", allowed_hosts=["127.0.0.1:8772"])
vault.put("bob@acme.example", "tracker", "trk-bob")
now = int(time.time())
for name, scope in [("alice", "tracker:read tracker:write"), ("bob", "tracker:read"),
                    ("carol", "tracker:read")]:
    token = jwt.encode({"iss": ISSUER, "sub": f"{name}@acme.example", "aud": resource,
                        "scope": scope, "iat": now, "exp": now + 3600},
                       key, algorithm="RS256")
    (out / f"{name}.jwt").write_text(token)
serve(idp, 8773)
serve(tracker_app, 8771)
serve(build_broker(cfg), 8772)
(out / "ready").write_text("ok")
while True:
    time.sleep(1)
_ = uvicorn
