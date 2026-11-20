import json
from pathlib import Path

import pytest
from cryptography.fernet import Fernet

from acme_broker.vault import Vault


def test_vault_encrypts_at_rest(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v.json", Fernet.generate_key())
    vault.put("alice@acme.example", "tracker", "trk-alice")
    raw = (tmp_path / "v.json").read_text()
    assert "trk-alice" not in raw
    assert vault.get("alice@acme.example", "tracker") == "trk-alice"
    assert oct((tmp_path / "v.json").stat().st_mode & 0o777) == "0o600"


def test_vault_key_mismatch_cannot_decrypt(tmp_path: Path) -> None:
    Vault(tmp_path / "v.json", Fernet.generate_key()).put("a", "tracker", "s")
    with pytest.raises(Exception):  # noqa: B017  (cryptography.fernet.InvalidToken)
        Vault(tmp_path / "v.json", Fernet.generate_key()).get("a", "tracker")


def test_revoke_removes_only_that_user(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v.json", Fernet.generate_key())
    vault.put("a", "tracker", "1")
    vault.put("b", "tracker", "2")
    assert vault.revoke_user("a") == 1
    assert list(json.loads((tmp_path / "v.json").read_text())) == ["b"]
