"""Per-user upstream credentials, encrypted at rest. Never leave the broker."""

from __future__ import annotations

import json
from pathlib import Path

from cryptography.fernet import Fernet


class Vault:
    def __init__(self, path: Path, key: bytes) -> None:
        self.path, self._fernet = path, Fernet(key)

    def _load(self) -> dict[str, dict[str, str]]:
        if not self.path.exists():
            return {}
        data: dict[str, dict[str, str]] = json.loads(self.path.read_text())
        return data

    def _save(self, data: dict[str, dict[str, str]]) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        tmp.chmod(0o600)
        tmp.replace(self.path)

    def put(self, user: str, system: str, secret: str) -> None:
        data = self._load()
        sealed = self._fernet.encrypt(secret.encode()).decode()
        data.setdefault(user, {})[system] = sealed
        self._save(data)

    def get(self, user: str, system: str) -> str | None:
        token = self._load().get(user, {}).get(system)
        return None if token is None else self._fernet.decrypt(token.encode()).decode()

    def revoke_user(self, user: str) -> int:
        """Delete every credential a user registered; returns how many."""
        data = self._load()
        removed = len(data.pop(user, {}))
        self._save(data)
        return removed
