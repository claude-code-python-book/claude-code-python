"""Validate Kubernetes manifests against the official OpenAPI v3 schemas.

The schemas come from kubernetes/kubernetes api/openapi-spec/v3 at v1.37.2.
Like `kubeconform -strict`, unknown fields are errors, so a misspelled key
such as `readinesProbe` fails instead of being silently ignored.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

# api/openapi-spec/v3 from a checkout of github.com/kubernetes/kubernetes
SPEC = Path(os.environ.get("K8S_OPENAPI_DIR", "kubernetes/api/openapi-spec/v3"))
FILES = ["api__v1_openapi.json", "apis__apps__v1_openapi.json", "apis__batch__v1_openapi.json"]


def _strict(node: Any) -> Any:
    if isinstance(node, dict):
        out = {k: _strict(v) for k, v in node.items()}
        if "properties" in out and "additionalProperties" not in out:
            out["additionalProperties"] = False
        return out
    if isinstance(node, list):
        return [_strict(v) for v in node]
    return node


def load() -> tuple[dict[str, Any], dict[tuple[str, str], str]]:
    schemas: dict[str, Any] = {}
    for name in FILES:
        schemas.update(json.loads((SPEC / name).read_text())["components"]["schemas"])
    kinds = {}
    for name, schema in schemas.items():
        for gvk in schema.get("x-kubernetes-group-version-kind", []):
            api = f"{gvk['group']}/{gvk['version']}" if gvk["group"] else gvk["version"]
            kinds[(api, gvk["kind"])] = name
    return _strict(schemas), kinds


SCHEMAS, KINDS = load()


def errors(doc: dict[str, Any]) -> list[str]:
    name = KINDS[(doc["apiVersion"], doc["kind"])]
    validator = Draft202012Validator(
        {"$ref": f"#/components/schemas/{name}", "components": {"schemas": SCHEMAS}}
    )
    return [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}"
            for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))]


def check_file(path: Path) -> list[str]:
    out = []
    for doc in yaml.safe_load_all(path.read_text()):
        if doc:
            out += [f"{path.name} {doc['kind']}: {msg}" for msg in errors(doc)]
    return out


if __name__ == "__main__":
    problems = [p for arg in sys.argv[1:] for p in check_file(Path(arg))]
    for arg in sys.argv[1:]:
        for doc in yaml.safe_load_all(Path(arg).read_text()):
            if doc:
                print(f"{Path(arg).name}: {doc['apiVersion']} {doc['kind']} {doc['metadata']['name']}")
    print("\n".join(problems) if problems else "valid against Kubernetes v1.37.2 schemas (strict)")
    sys.exit(1 if problems else 0)
