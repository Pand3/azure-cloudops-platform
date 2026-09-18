"""Environment-based configuration for the Platform API."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="PLATFORM_",
        extra="ignore",
    )

    app_name: str = Field(
        default="cloudops-platform-api",
        min_length=1,
    )
    app_version: str = Field(
        default="0.1.0",
        min_length=1,
    )
    environment: Literal["dev", "staging", "prod"] = "dev"


@lru_cache
def get_settings() -> Settings:
    """Load and cache application settings."""

    return Settings()
