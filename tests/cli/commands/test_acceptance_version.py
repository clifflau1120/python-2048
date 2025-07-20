"""Acceptance tests for the `version` command."""

import pytest
import typer.testing

from python_2048.cli import app
from python_2048.version import __version__


@pytest.fixture
def runner():
    return typer.testing.CliRunner()


def test_command(runner: typer.testing.CliRunner):
    result = runner.invoke(app.app, ["version"])

    assert result.exit_code == 0
    assert result.output.strip() == __version__
