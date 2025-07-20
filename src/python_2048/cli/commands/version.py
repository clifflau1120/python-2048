"""Module of the `version` command."""

import typer

from python_2048.version import __version__

app = typer.Typer()


@app.command()
def version():
    """Show the version of the application."""

    print(__version__)
