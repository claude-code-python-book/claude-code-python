"""Run the broker: python -m acme_broker (configuration from the environment)."""

import os
from pathlib import Path

import uvicorn

from .app import BrokerConfig, build_broker
from .audit import AuditLog
from .identity import IdpTokenVerifier, jwks_resolver
from .vault import Vault


def main() -> None:
    env = os.environ
    resource = env["ACME_BROKER_URL"]                 # https://mcp.acme.example/mcp
    cfg = BrokerConfig(
        issuer=env["ACME_IDP_ISSUER"],
        resource_url=resource,
        verifier=IdpTokenVerifier(env["ACME_IDP_ISSUER"], resource,
                                  jwks_resolver(env["ACME_IDP_JWKS_URL"])),
        vault=Vault(Path(env["ACME_VAULT_PATH"]), env["ACME_VAULT_KEY"].encode()),
        audit=AuditLog(Path(env["ACME_AUDIT_PATH"])),
        tracker_url=env["ACME_TRACKER_URL"],
        allowed_hosts=env["ACME_ALLOWED_HOSTS"].split(","),
    )
    uvicorn.run(build_broker(cfg), host="0.0.0.0", port=int(env.get("PORT", "8080")),  # noqa: S104
                proxy_headers=True)


if __name__ == "__main__":
    main()
