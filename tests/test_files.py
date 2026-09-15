"""Tests for CloudOps environment scaffolding."""

import json
from pathlib import Path

import pytest
import yaml

from cloudops.files import ScaffoldError, scaffold_environment


def test_dry_run_does_not_create_files(tmp_path: Path) -> None:
    """Dry-run should report planned files without writing anything."""

    output_directory = tmp_path / "environments"

    result = scaffold_environment(
        "dev",
        output_directory,
        dry_run=True,
    )

    assert result.created is False
    assert result.directory == output_directory / "dev"
    assert len(result.files) == 4
    assert not output_directory.exists()


def test_scaffold_creates_environment_files(tmp_path: Path) -> None:
    """Scaffolding should create valid YAML and JSON files."""

    output_directory = tmp_path / "environments"

    result = scaffold_environment("dev", output_directory)

    assert result.created is True
    assert all(path.exists() for path in result.files)

    cloudops_data = yaml.safe_load(
        (result.directory / "cloudops.yaml").read_text(encoding="utf-8")
    )
    terraform_data = json.loads(
        (result.directory / "terraform.tfvars.json").read_text(encoding="utf-8")
    )
    helm_data = yaml.safe_load(
        (result.directory / "values.yaml").read_text(encoding="utf-8")
    )

    assert cloudops_data["project"]["environment"] == "dev"
    assert cloudops_data["kubernetes"]["replicas"] == 1
    assert terraform_data["resource_group_name"] == "rg-cloudops-dev"
    assert helm_data["environment"] == "dev"


def test_reject_invalid_environment(tmp_path: Path) -> None:
    """Only recognised environment names should be accepted."""

    with pytest.raises(ScaffoldError, match="Invalid environment"):
        scaffold_environment("testing", tmp_path)


def test_refuse_to_overwrite_existing_files(tmp_path: Path) -> None:
    """Existing environment files must not be overwritten."""

    output_directory = tmp_path / "environments"
    scaffold_environment("dev", output_directory)

    with pytest.raises(ScaffoldError, match="Refusing to overwrite"):
        scaffold_environment("dev", output_directory)
