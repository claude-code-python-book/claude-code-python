"""Password hashing with pwdlib and Argon2, as the FastAPI docs recommend."""

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def hash_password(password: str) -> str:
    """Return an Argon2 hash of the password."""
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Return True if the password matches the hash."""
    return password_hash.verify(password, hashed)
