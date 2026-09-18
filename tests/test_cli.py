"""Tests for the CloudOps command-line interface."""

from typer.testing import CliRunner

from cloudops.cli import app

runner = CliRunner()


def test_version_command() -> None:
    """The version command should display the installed version."""

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "cloudops version 0.1.0" in result.output


def test_validate_config_command(tmp_path) -> None:
    """The config command should accept a valid YAML file."""

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
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
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["config", "validate", str(config_path)])

    assert result.exit_code == 0
    assert "Valid configuration" in result.output
    assert "Environment: dev" in result.output
    assert "Azure location: uksouth" in result.output
