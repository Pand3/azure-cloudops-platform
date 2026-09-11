"""Command-line interface for the CloudOps platform."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from cloudops import __version__
from cloudops.api import ApiCheckError, check_api
from cloudops.config import ConfigError, load_config
from cloudops.log_analyser import LogAnalysisError, analyse_log
from cloudops.logging_config import setup_logging

logger = logging.getLogger(__name__)

app = typer.Typer(
    name="cloudops",
    help="Operate and troubleshoot the Azure CloudOps platform.",
    no_args_is_help=True,
)

config_app = typer.Typer(help="Manage platform configuration.")
api_app = typer.Typer(help="Check platform APIs.")
logs_app = typer.Typer(help="Analyse platform logs.")

app.add_typer(config_app, name="config")
app.add_typer(api_app, name="api")
app.add_typer(logs_app, name="logs")


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


@api_app.command("check")
def check_api_command(
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
    """Check whether the configured REST API is healthy."""
    setup_logging()
    try:
        configuration = load_config(path)
        result = check_api(
            base_url=str(configuration.api.base_url),
            timeout_seconds=configuration.api.timeout_seconds,
        )
    except (ConfigError, ApiCheckError) as error:
        logger.error(
            "API health check failed",
            extra={
                "event": "api_check_failure",
                "config_path": str(path),
                "error": str(error),
            },
        )
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    logger.info(
        "API health check succeeded",
        extra={
            "event": "api_check_success",
            "url": result.url,
            "status_code": result.status_code,
            "response_time_ms": round(result.response_time_ms, 2),
            "config_path": str(path),
        },
    )
    json_keys = ", ".join(sorted(result.data))

    typer.echo(f"API healthy: {result.url}")
    typer.echo(f"HTTP status: {result.status_code}")
    typer.echo(f"Response time: {result.response_time_ms:.2f} ms")
    typer.echo(f"JSON object keys: {json_keys}")


@logs_app.command("analyse")
def analyse_logs_command(
    path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            readable=True,
            help="Path to the JSON Lines log file.",
        ),
    ] = Path("logs/cloudops.log"),
) -> None:
    """Analyse structured CloudOps log entries."""

    try:
        summary = analyse_log(path)
    except LogAnalysisError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    if summary.average_response_time_ms is None:
        average_response_time = "No data"
    else:
        average_response_time = f"{summary.average_response_time_ms:.2f} ms"

    status_codes = ", ".join(
        f"{code}: {count}" for code, count in sorted(summary.status_codes.items())
    )

    if not status_codes:
        status_codes = "No data"

    typer.echo(f"Log analysis: {path}")
    typer.echo(f"Total lines: {summary.total_lines}")
    typer.echo(f"Valid entries: {summary.valid_entries}")
    typer.echo(f"Malformed entries: {summary.malformed_entries}")
    typer.echo(f"Successful API checks: {summary.successful_checks}")
    typer.echo(f"Failed API checks: {summary.failed_checks}")
    typer.echo(f"Average response time: {average_response_time}")
    typer.echo(f"HTTP status codes: {status_codes}")


if __name__ == "__main__":
    app()
