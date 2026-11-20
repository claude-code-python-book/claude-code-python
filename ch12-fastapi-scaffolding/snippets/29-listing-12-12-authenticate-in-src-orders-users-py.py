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
