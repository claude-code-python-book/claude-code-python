"""Create and check JWT access tokens with PyJWT."""

from datetime import UTC, datetime, timedelta

import jwt

ALGORITHM = "HS256"


def create_access_token(
    subject: str, secret: str, minutes: int, now: datetime | None = None
) -> str:
    """Return a signed token for `subject` that expires after `minutes`."""
    issued = now or datetime.now(UTC)
    claims = {"sub": subject, "iat": issued, "exp": issued + timedelta(minutes=minutes)}
    return jwt.encode(claims, secret, algorithm=ALGORITHM)


def read_subject(token: str, secret: str) -> str:
    """Return the token's subject.

    Raises:
        jwt.InvalidTokenError: If the token is malformed, has a bad signature,
            has expired, or lacks an `exp` or `sub` claim.
    """
    claims = jwt.decode(
        token, secret, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]}
    )
    return str(claims["sub"])
