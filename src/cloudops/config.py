"""Load and validate CloudOps configuration files."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, ValidationError


class StrictModel(BaseModel):
    """Base model that rejects unknown configuration fields."""

    model_config = ConfigDict(extra="forbid")


class ProjectConfig(StrictModel):
    """General project configuration."""

    name: str = Field(min_length=1)
    environment: Literal["dev", "staging", "prod"]


class AzureConfig(StrictModel):
    """Azure resource configuration."""

    location: str = Field(min_length=1)
    resource_group: str = Field(min_length=1)


class KubernetesConfig(StrictModel):
    """Kubernetes workload configuration."""

    namespace: str = Field(min_length=1)
    replicas: int = Field(ge=1, le=10)


class ApiConfig(StrictModel):
    """REST API configuration."""

    base_url: HttpUrl
    timeout_seconds: int = Field(gt=0, le=60)


class PlatformConfig(StrictModel):
    """Complete CloudOps platform configuration."""

    project: ProjectConfig
    azure: AzureConfig
    kubernetes: KubernetesConfig
    api: ApiConfig


class ConfigError(Exception):
    """Raised when configuration loading or validation fails."""


def load_config(path: Path) -> PlatformConfig:
    """Load and validate a YAML configuration file."""

    try:
        with path.open(encoding="utf-8") as file:
            raw_config = yaml.safe_load(file)
    except OSError as error:
        raise ConfigError(f"Could not read {path}: {error}") from error
    except yaml.YAMLError as error:
        raise ConfigError(f"Invalid YAML in {path}: {error}") from error

    if not isinstance(raw_config, dict):
        raise ConfigError("The configuration must contain a YAML mapping.")

    try:
        return PlatformConfig.model_validate(raw_config)
    except ValidationError as error:
        raise ConfigError(f"Configuration validation failed:\n{error}") from error
