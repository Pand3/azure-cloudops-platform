"""Command-line interface for the CloudOps platform."""

from pathlib import Path
from typing import Annotated

import typer

from cloudops import __version__
from cloudops.config import ConfigError, load_config

app = typer.Typer(
    name="cloudops",
    help="Operate and troubleshoot the Azure CloudOps platform.",
    no_args_is_help=True,
)
config_app = typer.Typer(help="Manage platform configuration.")
app.add_typer(config_app, name="config")


@app.callback()
def main() -> None:
    """Operate and troubleshoot the Azure CloudOps platform."""


@app.command()
def version() -> None:
    """Display the installed CloudOps CLI version."""
    typer.echo(f"cloudops version {__version__}")


@config_app.command("validate")
def validate_config(
    path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            readable=True,
            help="Path to the YAML configuration file.",
        ),
    ] = Path("config/example.yaml"),
) -> None:
    """Validate a CloudOps YAML configuration file."""

    try:
        configuration = load_config(path)
    except ConfigError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Valid configuration: {path}")
    typer.echo(f"Environment: {configuration.project.environment}")
    typer.echo(f"Azure location: {configuration.azure.location}")
    typer.echo(f"Kubernetes namespace: {configuration.kubernetes.namespace}")


if __name__ == "__main__":
    app()
