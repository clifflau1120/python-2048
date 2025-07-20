"""Unit tests for the move and merge logic on a game board."""

import copy

import pytest

from python_2048.game import types
from python_2048.game.lib import board_utils


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param(
            [[None], [4], [None]],
            [[4], [None], [None]],
            id="regular-board-moveable",
        ),
        pytest.param(
            [[4], [4], [None]],
            [[8], [None], [None]],
            id="regular-board-mergeable",
        ),
        pytest.param(
            [[None], [4], [4]],
            [[8], [None], [None]],
            id="regular-board-moveable-and-mergeable",
        ),
    ],
)
def test_move_and_merge_up__effective(board: types.GameBoard, expected: types.GameBoard):
    assert board_utils.move_and_merge_up(board)
    assert board == expected


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([], id="empty-board"),
        pytest.param([[None]], id="unit-board-empty"),
        pytest.param([[2]], id="unit-board-full"),
        pytest.param(
            [[4], [None], [None]],
            id="regular-board",
        ),
    ],
)
def test_move_and_merge_up__not_moveable_nor_mergeable(board: types.GameBoard):
    not_changed = copy.deepcopy(board)

    assert not board_utils.move_and_merge_up(board)
    assert board == not_changed


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param(
            [[None, 4, None]],
            [[4, None, None]],
            id="regular-board-moveable",
        ),
        pytest.param(
            [[4, 4, None]],
            [[8, None, None]],
            id="regular-board-mergeable",
        ),
        pytest.param(
            [[None, 4, 4]],
            [[8, None, None]],
            id="regular-board-moveable-and-mergeable",
        ),
    ],
)
def test_move_and_merge_left__effective(board: types.GameBoard, expected: types.GameBoard):
    assert board_utils.move_and_merge_left(board)
    assert board == expected


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([], id="empty-board"),
        pytest.param([[None]], id="unit-board-empty"),
        pytest.param([[2]], id="unit-board-full"),
        pytest.param(
            [[4, None, None]],
            id="regular-board",
        ),
    ],
)
def test_move_and_merge_left__not_moveable_nor_mergeable(board: types.GameBoard):
    not_changed = copy.deepcopy(board)

    assert not board_utils.move_and_merge_left(board)
    assert board == not_changed


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param(
            [[None], [4], [None]],
            [[None], [None], [4]],
            id="regular-board-moveable",
        ),
        pytest.param(
            [[None], [4], [4]],
            [[None], [None], [8]],
            id="regular-board-mergeable",
        ),
        pytest.param(
            [[4], [4], [None]],
            [[None], [None], [8]],
            id="regular-board-moveable-and-mergeable",
        ),
    ],
)
def test_move_and_merge_down__effective(board: types.GameBoard, expected: types.GameBoard):
    assert board_utils.move_and_merge_down(board)
    assert board == expected


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([], id="empty-board"),
        pytest.param([[None]], id="unit-board-empty"),
        pytest.param([[2]], id="unit-board-full"),
        pytest.param(
            [[None], [None], [4]],
            id="regular-board",
        ),
    ],
)
def test_move_and_merge_down__not_moveable_nor_mergeable(board: types.GameBoard):
    not_changed = copy.deepcopy(board)

    assert not board_utils.move_and_merge_down(board)
    assert board == not_changed


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param(
            [[None, 4, None]],
            [[None, None, 4]],
            id="regular-board-moveable",
        ),
        pytest.param(
            [[None, 4, 4]],
            [[None, None, 8]],
            id="regular-board-mergeable",
        ),
        pytest.param(
            [[4, 4, None]],
            [[None, None, 8]],
            id="regular-board-moveable-and-mergeable",
        ),
    ],
)
def test_move_and_merge_right__effective(board: types.GameBoard, expected: types.GameBoard):
    assert board_utils.move_and_merge_right(board)
    assert board == expected


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([], id="empty-board"),
        pytest.param([[None]], id="unit-board-empty"),
        pytest.param([[2]], id="unit-board-full"),
        pytest.param(
            [[None, None, 4]],
            id="regular-board",
        ),
    ],
)
def test_move_and_merge_right__not_moveable_nor_mergeable(board: types.GameBoard):
    not_changed = copy.deepcopy(board)

    assert not board_utils.move_and_merge_right(board)
    assert board == not_changed
