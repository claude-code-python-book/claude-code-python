"""API users and the password check, independent of HTTP."""

import threading
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Someone who can call the API on behalf of one customer."""

    username: str
    customer_id: str
    hashed_password: str
    disabled: bool = False


class InMemoryUserRepository:
    """Users kept in memory, for tests and local development."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._lock = threading.Lock()

    def add(self, user: User) -> None:
        """Store a user, replacing any user with the same name."""
        with self._lock:
            self._users[user.username] = user

    def get(self, username: str) -> User | None:
        """Return the user, or None."""
        return self._users.get(username)


def authenticate(
    users: InMemoryUserRepository,
    username: str,
    password: str,
    *,
    verify: Callable[[str, str], bool],
    dummy_hash: str,
) -> User | None:
    """Return the user if the password matches and the account is active.

    An unknown username is checked against `dummy_hash`, so it takes about as
    long as a wrong password and response times don't reveal valid names.
    """
    user = users.get(username)
    if user is None:
        verify(password, dummy_hash)
        return None
    if not verify(password, user.hashed_password) or user.disabled:
        return None
    return user
