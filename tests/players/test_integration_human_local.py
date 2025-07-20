"""Integration tests for `LocalHumanPlayer`."""

from unittest import mock

import pytest

from python_2048.game import types
from python_2048.players import human_local


@pytest.mark.parametrize(
    ["keystroke", "direction"],
    [
        pytest.param("w", types.SlideDirection.UP, id="w"),
        pytest.param("a", types.SlideDirection.LEFT, id="a"),
        pytest.param("s", types.SlideDirection.DOWN, id="s"),
        pytest.param("d", types.SlideDirection.RIGHT, id="d"),
    ],
)
@mock.patch.object(human_local.LocalHumanPlayer, "_prompt_for_option")
def test_get_next_move__press_wasd__returns_slide_direction(
    mock_prompt_for_option: mock.MagicMock,
    keystroke: str,
    direction: types.SlideDirection,
):
    # given:
    board = mock.Mock()
    player = human_local.LocalHumanPlayer()
    mock_prompt_for_option.return_value = keystroke

    # when
    assert player.get_next_move(board).direction == direction


@mock.patch.object(human_local.LocalHumanPlayer, "_save_game")
@mock.patch.object(human_local.LocalHumanPlayer, "_prompt_for_option")
def test_get_next_move__press_p__calls_save_game(
    mock_prompt_for_option: mock.MagicMock,
    mock_save_game: mock.MagicMock,
):
    # given:
    board = mock.Mock()
    player = human_local.LocalHumanPlayer()
    mock_prompt_for_option.side_effect = "pw"

    # when
    _ = player.get_next_move(board)

    # then:
    mock_save_game.assert_called_once_with(board)


@mock.patch.object(human_local.LocalHumanPlayer, "_quit_game")
@mock.patch.object(human_local.LocalHumanPlayer, "_prompt_for_option")
def test_get_next_move__press_q__calls_quit_game(
    mock_prompt_for_option: mock.MagicMock,
    mock_quit_game: mock.MagicMock,
):
    # given:
    board = mock.Mock()
    player = human_local.LocalHumanPlayer()
    mock_prompt_for_option.side_effect = "qw"

    # when
    _ = player.get_next_move(board)

    # then:
    mock_quit_game.assert_called_once()


@mock.patch.object(human_local.LocalHumanPlayer, "_prompt_for_option")
def test_get_next_move__unrecognized_option__prompts_until_valid(
    mock_prompt_for_option: mock.MagicMock,
):
    # given:
    board = mock.Mock()
    player = human_local.LocalHumanPlayer()
    mock_prompt_for_option.side_effect = ["x", "y", "z", "w"]

    # when:
    assert player.get_next_move(board).direction == types.SlideDirection.UP
