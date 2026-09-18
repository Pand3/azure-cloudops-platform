"""Filesystem scaffolding for CloudOps environments."""

import json
from dataclasses import dataclass
from pathlib import Path

import yaml

VALID_ENVIRONMENTS = {"dev", "staging", "prod"}


@dataclass(frozen=True)
class ScaffoldResult:
    """Result of an environment scaffolding operation."""

    environment: str
    directory: Path
    files: tuple[Path, ...]
    created: bool


class ScaffoldError(Exception):
    """Raised when environment scaffolding cannot be completed."""


def scaffold_environment(
    environment: str,
    output_directory: Path,
    *,
    dry_run: bool = False,
) -> ScaffoldResult:
    """Create configuration files for a CloudOps environment."""

    if environment not in VALID_ENVIRONMENTS:
        valid_values = ", ".join(sorted(VALID_ENVIRONMENTS))
        raise ScaffoldError(
            f"Invalid environment '{environment}'. Expected one of: {valid_values}"
        )

    environment_directory = output_directory / environment

    cloudops_path = environment_directory / "cloudops.yaml"
    terraform_path = environment_directory / "terraform.tfvars.json"
    helm_path = environment_directory / "values.yaml"
    readme_path = environment_directory / "README.md"

    target_files = (
        cloudops_path,
        terraform_path,
        helm_path,
        readme_path,
    )

    existing_files = [path for path in target_files if path.exists()]

    if existing_files:
        existing_names = ", ".join(str(path) for path in existing_files)
        raise ScaffoldError(f"Refusing to overwrite existing files: {existing_names}")

    if dry_run:
        return ScaffoldResult(
            environment=environment,
            directory=environment_directory,
            files=target_files,
            created=False,
        )

    cloudops_config = {
        "project": {
            "name": "azure-cloudops-platform",
            "environment": environment,
        },
        "azure": {
            "location": "uksouth",
            "resource_group": f"rg-cloudops-{environment}",
        },
        "kubernetes": {
            "namespace": f"cloudops-{environment}",
            "replicas": 1 if environment == "dev" else 2,
        },
        "api": {
            "base_url": "http://127.0.0.1:8000",
            "health_path": "/health",
            "timeout_seconds": 10,
        },
    }

    terraform_variables = {
        "environment": environment,
        "location": "uksouth",
        "resource_group_name": f"rg-cloudops-{environment}",
    }

    helm_values = {
        "environment": environment,
        "replicaCount": 1 if environment == "dev" else 2,
        "image": {
            "repository": "replace-with-acr-name.azurecr.io/platform-api",
            "tag": "latest",
        },
    }

    readme_content = f"""# {environment.title()} Environment

Generated configuration for the `{environment}` CloudOps environment.

Do not store credentials or secrets in these files.
"""

    try:
        environment_directory.mkdir(parents=True, exist_ok=True)

        cloudops_path.write_text(
            yaml.safe_dump(cloudops_config, sort_keys=False),
            encoding="utf-8",
        )
        terraform_path.write_text(
            json.dumps(terraform_variables, indent=2) + "\n",
            encoding="utf-8",
        )
        helm_path.write_text(
            yaml.safe_dump(helm_values, sort_keys=False),
            encoding="utf-8",
        )
        readme_path.write_text(readme_content, encoding="utf-8")
    except OSError as error:
        raise ScaffoldError(
            f"Could not scaffold {environment_directory}: {error}"
        ) from error

    return ScaffoldResult(
        environment=environment,
        directory=environment_directory,
        files=target_files,
        created=True,
    )
