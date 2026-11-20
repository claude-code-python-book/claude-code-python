"""Settings read from ORDERS_* environment variables with pydantic-settings."""

from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Everything that differs between environments."""

    model_config = SettingsConfigDict(env_prefix="ORDERS_")

    environment: Literal["dev", "test", "prod"] = "dev"
    jwt_secret: SecretStr = Field(min_length=32)
    token_minutes: int = Field(default=30, ge=1, le=1440)
    cors_origins: list[str] = []
    demo_password: SecretStr | None = None

    @model_validator(mode="after")
    def no_demo_user_in_prod(self) -> Self:
        """Refuse to start production with the demo account enabled."""
        if self.environment == "prod" and self.demo_password is not None:
            raise ValueError("ORDERS_DEMO_PASSWORD must not be set in prod")
        return self
