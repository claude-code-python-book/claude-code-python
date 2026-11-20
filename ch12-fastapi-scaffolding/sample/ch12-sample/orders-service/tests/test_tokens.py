from datetime import UTC, datetime, timedelta

import jwt
import pytest

from orders.tokens import ALGORITHM, create_access_token, read_subject

SECRET = "test-secret-that-is-at-least-32-bytes-long"


def test_a_fresh_token_names_its_subject() -> None:
    assert read_subject(create_access_token("alice", SECRET, 30), SECRET) == "alice"


def test_an_expired_token_is_rejected() -> None:
    issued = datetime.now(UTC) - timedelta(minutes=31)
    token = create_access_token("alice", SECRET, 30, now=issued)
    with pytest.raises(jwt.ExpiredSignatureError):
        read_subject(token, SECRET)


def test_a_token_signed_with_another_key_is_rejected() -> None:
    token = create_access_token("alice", "another-secret-that-is-32-bytes-long", 30)
    with pytest.raises(jwt.InvalidSignatureError):
        read_subject(token, SECRET)


def test_a_token_without_a_subject_is_rejected() -> None:
    exp = datetime.now(UTC) + timedelta(minutes=5)
    token = jwt.encode({"exp": exp}, SECRET, algorithm=ALGORITHM)
    with pytest.raises(jwt.MissingRequiredClaimError):
        read_subject(token, SECRET)


def test_an_unsigned_token_is_rejected() -> None:
    exp = datetime.now(UTC) + timedelta(minutes=5)
    token = jwt.encode({"sub": "alice", "exp": exp}, "", algorithm="none")
    with pytest.raises(jwt.InvalidAlgorithmError):
        read_subject(token, SECRET)
