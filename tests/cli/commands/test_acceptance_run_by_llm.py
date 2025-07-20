"""
Acceptance tests for the `run` command impersonated by an LLM.

Since there is no frontend/backend separation in this codebase,
acceptance tests look a lot like robot tests.
"""

import inspect
import json
import pathlib
from unittest import mock

import pytest
import typer.testing

from python_2048.cli import app
from python_2048.game import types
from python_2048.players import llm

MOCK_MODEL_NAME = "some-llm-model"


@pytest.fixture
def runner():
    return typer.testing.CliRunner()


@mock.patch.object(llm, "LlmPlayer")
def test_command__play_by_llm(llm_player_cls: mock.MagicMock, runner: typer.testing.CliRunner):
    # given:
    function_name = inspect.currentframe().f_code.co_name  # type: ignore

    board = [
        [1024, 1024, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    file_path = pathlib.Path(f"/tmp/{function_name}.json")
    file_path.unlink(missing_ok=True)
    file_path.write_text(json.dumps(board))

    # given: an AI Assitant
    llm_player = llm_player_cls.return_value
    llm_player.get_next_move.return_value = types.PlayerDecision(
        direction=types.SlideDirection.LEFT, reason="Slide to left to win."
    )

    # when:
    result = runner.invoke(
        app.app,
        ["run", str(file_path), "--impersonate", "--model", MOCK_MODEL_NAME],
    )

    # then:
    assert "You selected: LEFT" in result.output
    assert "Reason provided: Slide to left to win." in result.output
    assert "Congratulations, you win" in result.output
    assert result.exit_code == 0
