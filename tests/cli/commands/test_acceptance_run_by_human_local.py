"""
Acceptance tests for the `run` command with a human player.

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
from python_2048.configurations import file_utils
from python_2048.game import types
from python_2048.players import llm

MOCK_MODEL_NAME = "some-llm-model"


@pytest.fixture
def runner():
    return typer.testing.CliRunner()


def test_command__new_game(runner: typer.testing.CliRunner):
    # when:
    result = runner.invoke(
        app.app,
        ["run", "--seed", "1"],
        input="adadadadadadadadadadadsssadadadasasdassdsdassasssdasssdaassdadadadada",
    )

    # then:
    assert "Score: 158" in result.output
    assert "Game over" in result.output
    assert result.exit_code == 0


def test_command__continue_game__then_lose(runner: typer.testing.CliRunner):
    # given:
    function_name = inspect.currentframe().f_code.co_name  # type: ignore

    board = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]

    file_path = pathlib.Path(f"/tmp/{function_name}.json")
    file_path.unlink(missing_ok=True)
    file_path.write_text(json.dumps(board))

    # when:
    result = runner.invoke(app.app, ["run", str(file_path)])

    # then:
    assert "Score: 48" in result.output
    assert "Game over" in result.output
    assert result.exit_code == 0


def test_command__continue_game__then_win(runner: typer.testing.CliRunner):
    # given:
    function_name = inspect.currentframe().f_code.co_name  # type: ignore

    board = [
        [2048, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    file_path = pathlib.Path(f"/tmp/{function_name}.json")
    file_path.unlink(missing_ok=True)
    file_path.write_text(json.dumps(board))

    # when:
    result = runner.invoke(app.app, ["run", str(file_path)])

    # then:
    assert "Score: 2048" in result.output
    assert "Congratulations, you win" in result.output
    assert result.exit_code == 0


def test_command__continue_game__with_invalid_snapshot(runner: typer.testing.CliRunner):
    # given:
    function_name = inspect.currentframe().f_code.co_name  # type: ignore

    file_path = pathlib.Path(f"/tmp/{function_name}.json")
    file_path.unlink(missing_ok=True)
    file_path.write_text("not-json")

    # when:
    result = runner.invoke(app.app, ["run", str(file_path)])

    # then:
    assert "There is an error in the game snapshot file" in result.output
    assert result.exit_code == 1


def test_command__continue_game__with_invalid_board(runner: typer.testing.CliRunner):
    # given:
    function_name = inspect.currentframe().f_code.co_name  # type: ignore

    board = [
        [None, None, None, None],
        [None, None, None],
        [None, None],
        [None],
    ]

    file_path = pathlib.Path(f"/tmp/{function_name}.json")
    file_path.unlink(missing_ok=True)
    file_path.write_text(json.dumps(board))

    # when:
    result = runner.invoke(app.app, ["run", str(file_path)])

    # then:
    assert "The game ran into an invalid state" in result.output
    assert result.exit_code == 1


def test_command__without_model__ai_suggestions__warns_user(runner: typer.testing.CliRunner):
    # when:
    result = runner.invoke(
        app.app,
        ["run", "--seed", "1"],
        input="hqy",
    )

    # then:
    assert "No AI Assistant is configured." in result.output
    assert result.exit_code == 0


@mock.patch.object(llm, "LlmPlayer")
def test_command__ai_suggestions(llm_player_cls: mock.MagicMock, runner: typer.testing.CliRunner):
    # given:
    llm_player = llm_player_cls.return_value
    llm_player.get_next_move.return_value = types.PlayerDecision(
        direction=types.SlideDirection.RIGHT,
        reason="Slide to right to maximize tile values and organize the board.",
    )

    # when:
    result = runner.invoke(
        app.app,
        ["run", "--seed", "1", "--model", MOCK_MODEL_NAME],
        input="hqy",
    )

    # then:
    assert "The AI Assistant suggested: RIGHT" in result.output
    assert (
        "Reason provided: Slide to right to maximize tile values and organize the board."
        in result.output
    )
    assert result.exit_code == 0


@mock.patch.object(file_utils, "try_write_game_snapshot")
def test_command__save_game__succeeded(
    mock_try_write_game_snapshot: mock.MagicMock,
    runner: typer.testing.CliRunner,
):
    # given:
    file_path = pathlib.Path("/tmp/python-2048-test-save-game-succeeded.json")
    mock_try_write_game_snapshot.return_value = True

    # when:
    result = runner.invoke(
        app.app,
        ["run"],
        input=f"p{file_path}\nqy\n",
    )

    # then:
    assert f"Wrote the game snapshot: {file_path}" in result.output
    assert result.exit_code == 0


@mock.patch.object(file_utils, "try_write_game_snapshot")
def test_command__save_game__failed(
    mock_try_write_game_snapshot: mock.MagicMock,
    runner: typer.testing.CliRunner,
):
    # given:
    file_path = pathlib.Path("/tmp/python-2048-test-save-game-failed.json")
    mock_try_write_game_snapshot.return_value = False

    # when:
    result = runner.invoke(
        app.app,
        ["run"],
        input=f"p{file_path}\nqy\n",
    )

    # then:
    assert f"Failed to write the game snapshot: {file_path}" in result.output
    assert result.exit_code == 0


def test_command__quit_game__confirmed(runner: typer.testing.CliRunner):
    # when:
    with mock.patch("pathlib.Path.open"):
        result = runner.invoke(
            app.app,
            ["run", "--seed", "1"],
            input="qy\n",
        )

    # then:
    assert "See you next time" in result.output
    assert result.exit_code == 0


def test_command__quit_game__unconfirmed(runner: typer.testing.CliRunner):
    # when:
    with mock.patch("pathlib.Path.open"):
        result = runner.invoke(
            app.app,
            ["run", "--seed", "1"],
            input="qn\nqy\n",
        )

    # then:
    assert "Let's continue the game" in result.output
    assert result.exit_code == 0
