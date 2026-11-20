"""The OAuth2 password flow: trade a username and password for a token."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from orders.deps import SettingsDep, UsersDep
from orders.passwords import DUMMY_HASH, verify_password
from orders.schemas import Token
from orders.tokens import create_access_token
from orders.users import authenticate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", summary="Get an access token")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: SettingsDep,
    users: UsersDep,
) -> Token:
    """Check the credentials and return a bearer token."""
    user = authenticate(
        users,
        form.username,
        form.password,
        verify=verify_password,
        dummy_hash=DUMMY_HASH,
    )
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    secret = settings.jwt_secret.get_secret_value()
    token = create_access_token(user.username, secret, settings.token_minutes)
    # "bearer" is the token type OAuth2 defines, not a password.
    return Token(access_token=token, token_type="bearer")  # noqa: S106
