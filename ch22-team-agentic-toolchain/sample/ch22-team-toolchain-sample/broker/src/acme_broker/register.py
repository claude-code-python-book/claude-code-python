"""Store your personal tracker token in the broker, once per token rotation.

    ACME_ID_TOKEN=$(acme-sso token --audience $ACME_BROKER_URL) \\
        python -m acme_broker.register https://mcp.acme.example
"""

import getpass
import os
import sys

import httpx2


def register(broker: str, id_token: str, secret: str, system: str = "tracker") -> int:
    resp = httpx2.put(f"{broker.rstrip('/')}/credentials/{system}",
                      json={"token": secret},
                      headers={"Authorization": f"Bearer {id_token}"}, timeout=10)
    return resp.status_code


if __name__ == "__main__":
    status = register(sys.argv[1], os.environ["ACME_ID_TOKEN"],
                      getpass.getpass("Personal tracker token: "))
    print("stored" if status == 200 else f"failed: HTTP {status}")
    sys.exit(status != 200)
