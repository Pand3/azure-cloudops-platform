"""Command-line interface for the CloudOps platform."""

import typer

from cloudops import __version__

app = typer.Typer(
    name="cloudops",
    help="Operate and troubleshoot the Azure CloudOps platform.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Operate and troubleshoot the Azure CloudOps platform."""


@app.command()
def version() -> None:
    """Display the installed CloudOps CLI version."""
    typer.echo(f"cloudops version {__version__}")


if __name__ == "__main__":
    app()
