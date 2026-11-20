"""Dependencies that path operations declare with Depends."""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from orders.config import Settings
from orders.service import OrderService
from orders.tokens import read_subject
from orders.users import InMemoryUserRepository, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_settings(request: Request) -> Settings:
    """Return the settings the app was created with."""
    settings: Settings = request.app.state.settings
    return settings


def get_users(request: Request) -> InMemoryUserRepository:
    """Return the user store."""
    users: InMemoryUserRepository = request.app.state.users
    return users


def get_order_service(request: Request) -> OrderService:
    """Return an OrderService backed by the app's repository."""
    return OrderService(request.app.state.orders)


SettingsDep = Annotated[Settings, Depends(get_settings)]
UsersDep = Annotated[InMemoryUserRepository, Depends(get_users)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: SettingsDep,
    users: UsersDep,
) -> User:
    """Return the user named in a valid bearer token, or fail with 401."""
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = read_subject(token, settings.jwt_secret.get_secret_value())
    except jwt.InvalidTokenError:
        raise unauthorized from None
    user = users.get(username)
    if user is None or user.disabled:
        raise unauthorized
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
