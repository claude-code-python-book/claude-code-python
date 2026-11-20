"""Write the OpenAPI schema to openapi.json, so API changes show up in review."""

import json
from pathlib import Path

from orders.app import create_app
from orders.config import Settings

settings = Settings(environment="test", jwt_secret="x" * 32)
schema = create_app(settings).openapi()
Path("openapi.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
print(f"wrote openapi.json: {len(schema['paths'])} paths")
