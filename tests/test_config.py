"""Tests for configuration loading and validation."""

from pathlib import Path

import pytest

from cloudops.config import ConfigError, load_config

VALID_CONFIG = """
project:
  name: azure-cloudops-platform
  environment: dev

azure:
  location: uksouth
  resource_group: rg-cloudops-dev

kubernetes:
  namespace: cloudops
  replicas: 2

api:
  base_url: https://example.com
  health_path: /health
  timeout_seconds: 10
"""


def write_config(tmp_path: Path, content: str) -> Path:
    """Write test configuration to a temporary file."""

    config_path = tmp_path / "config.yaml"
    config_path.write_text(content, encoding="utf-8")
    return config_path


def test_load_valid_config(tmp_path: Path) -> None:
    """A valid YAML file should produce a PlatformConfig object."""

    config_path = write_config(tmp_path, VALID_CONFIG)

    config = load_config(config_path)

    assert config.project.name == "azure-cloudops-platform"
    assert config.project.environment == "dev"
    assert config.azure.location == "uksouth"
    assert config.kubernetes.replicas == 2
    assert config.api.base_url.host == "example.com"


def test_reject_invalid_replica_count(tmp_path: Path) -> None:
    """Replica counts below one should be rejected."""

    invalid_config = VALID_CONFIG.replace("replicas: 2", "replicas: 0")
    config_path = write_config(tmp_path, invalid_config)

    with pytest.raises(ConfigError, match="Configuration validation failed"):
        load_config(config_path)


def test_reject_malformed_yaml(tmp_path: Path) -> None:
    """Malformed YAML should produce a configuration error."""

    config_path = write_config(tmp_path, "project: [")

    with pytest.raises(ConfigError, match="Invalid YAML"):
        load_config(config_path)


def test_reject_non_mapping_yaml(tmp_path: Path) -> None:
    """The configuration root must be a YAML mapping."""

    config_path = write_config(tmp_path, "- first\n- second\n")

    with pytest.raises(ConfigError, match="must contain a YAML mapping"):
        load_config(config_path)


def test_reject_missing_file(tmp_path: Path) -> None:
    """A missing configuration file should produce a readable error."""

    missing_path = tmp_path / "missing.yaml"

    with pytest.raises(ConfigError, match="Could not read"):
        load_config(missing_path)


def test_reject_health_path_without_leading_slash(tmp_path: Path) -> None:
    """The health path must begin with a forward slash."""

    invalid_config = VALID_CONFIG.replace(
        "health_path: /health",
        "health_path: health",
    )
    config_path = write_config(tmp_path, invalid_config)

    with pytest.raises(ConfigError, match="Configuration validation failed"):
        load_config(config_path)
