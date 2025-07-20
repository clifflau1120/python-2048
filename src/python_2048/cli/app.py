"""Module of the CLI application."""

import logging

import typer
import typing_extensions

from python_2048.cli.commands.run import app as run_command
from python_2048.cli.commands.version import app as version_command
from python_2048.configurations import log_utils

app = typer.Typer()
app.add_typer(run_command)
app.add_typer(version_command)


@app.callback()
def callback(
    debug: typing_extensions.Annotated[bool, typer.Option()] = False,
):
    log_utils.remove_default_sink()
    log_utils.add_file_as_sink(level=logging.DEBUG if debug else logging.INFO)


if __name__ == "__main__":  # pragma: no cover
    app()
