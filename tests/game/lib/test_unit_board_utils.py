"""Unit tests for the game logic related to the board."""

import random
from unittest import mock

import pytest

from python_2048.game import types
from python_2048.game.lib import board_utils

RANDOM_SEED = 100


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "create_empty_board")
def test_create_new_board__fixed_number_of_tiles(
    mock_create_empty_board: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board_size = 4
    new_tiles = mock.Mock()
    num_initial_tiles = 5

    # when:
    board = board_utils.create_new_board(board_size, new_tiles, num_initial_tiles)

    # then: the board should be instantiated
    mock_create_empty_board.assert_called_once_with(board_size)
    assert board == mock_create_empty_board.return_value

    # then: should spawn the expected number of tiles
    mock_spawn_new_tile.assert_called_with(board, new_tiles)
    assert mock_spawn_new_tile.call_count == num_initial_tiles


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "create_empty_board")
def test_create_new_board__random_number_of_tiles(
    mock_create_empty_board: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board_size = 4
    new_tiles = mock.Mock()

    random.seed(RANDOM_SEED)
    num_initial_tiles = None  # signifies a random number of tiles
    expected_number_of_tiles = 3  # from a constant seed

    # when:
    board = board_utils.create_new_board(board_size, new_tiles, num_initial_tiles)

    # then: the board should be instantiated
    mock_create_empty_board.assert_called_once_with(board_size)
    assert board == mock_create_empty_board.return_value

    # then: should spawn the expected number of tiles
    mock_spawn_new_tile.assert_called_with(board, new_tiles)
    assert mock_spawn_new_tile.call_count == expected_number_of_tiles


@pytest.mark.parametrize(
    ["board_size"],
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
    ],
)
def test_create_empty_board__non_positive_board_size(board_size: int):
    assert not board_utils.create_empty_board(board_size)


@pytest.mark.parametrize(
    ["board_size", "expected"],
    [
        pytest.param(1, [[None]], id="unit-board"),
        pytest.param(
            4,
            [
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
            ],
            id="regular-board",
        ),
    ],
)
def test_create_empty_board__positive_board_size(board_size: int, expected: types.GameBoard):
    board = board_utils.create_empty_board(board_size)
    assert board == expected


def test_spawn_new_tile__empty_board():
    # given:
    board: types.GameBoard = []

    # when:
    board_utils.spawn_new_tile(board)

    # then:
    assert not board


def test_spawn_new_tile__unit_board():
    # given
    random.seed(RANDOM_SEED)

    board: types.GameBoard = [[None]]
    new_tiles = (
        types.NewTile(value=2, weight=0.5),
        types.NewTile(value=4, weight=0.5),
    )

    # when:
    board_utils.spawn_new_tile(board, new_tiles)

    # then:
    assert board == [[2]]


def test_spawn_new_tile__regular_board():
    # given
    random.seed(RANDOM_SEED)

    board: types.GameBoard = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    new_tiles = (
        types.NewTile(value=2, weight=0.5),
        types.NewTile(value=4, weight=0.5),
    )

    # when:
    board_utils.spawn_new_tile(board, new_tiles)

    # then:
    assert board == [
        [None, None, None, None],
        [None, None, None, 2],
        [None, None, None, None],
        [None, None, None, None],
    ]


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param([], 0, id="empty-board"),
        pytest.param([[None]], 0, id="unit-board-empty"),
        pytest.param([[4]], 4, id="unit-board-full"),
        pytest.param(
            [
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
            ],
            40,
            id="regular-board",
        ),
    ],
)
def test_score(board: types.GameBoard, expected: int):
    assert board_utils.get_score(board) == expected


def test_has_2048__empty_board():
    board: types.GameBoard = []
    assert not board_utils.has_2048(board)


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param([[2048]], True, id="true"),
        pytest.param([[2]], False, id="false-int"),
        pytest.param([[None]], False, id="false-None"),
    ],
)
def test_has_2048__unit_board(board: types.GameBoard, expected: bool):
    assert board_utils.has_2048(board) == expected


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param(
            [
                [None, None, None, None],
                [2, None, None, None],
                [None, None, None, 4],
                [None, None, 2, 2048],
            ],
            True,
            id="true",
        ),
        pytest.param(
            [
                [None, None, None, None],
                [2, None, None, None],
                [None, None, None, 4],
                [None, None, 2, 4],
            ],
            False,
            id="false",
        ),
    ],
)
def test_has_2048__regular_board(board: types.GameBoard, expected: bool):
    assert board_utils.has_2048(board) == expected


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([], id="empty-board"),
        pytest.param([[2]], id="unit-board-full"),
        pytest.param([[None]], id="unit-board-empty"),
        pytest.param(
            [
                [2, 4, 2, 4],
                [4, 2, 4, 2],
                [2, 4, 2, 4],
                [4, 2, 4, 2],
            ],
            id="regular-board-full",
        ),
        pytest.param(
            [
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
            ],
            id="regular-board-empty",
        ),
    ],
)
def test_is_out_of_moves__not_moveable_nor_mergeable__returns_true(board: types.GameBoard):
    assert board_utils.is_out_of_moves(board)


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([[None], [2]], id="top"),
        pytest.param([[None, 2]], id="left"),
        pytest.param([[2, None]], id="right"),
        pytest.param([[2], [None]], id="bottom"),
    ],
)
def test_is_out_of_moves__moveable__returns_false(board: types.GameBoard):
    assert not board_utils.is_out_of_moves(board)


@pytest.mark.parametrize(
    ["board"],
    [
        pytest.param([[2, 2]], id="horizontally-adjacent"),
        pytest.param([[2, None, 2]], id="horizontally-separated-by-empty-tiles"),
        pytest.param([[2], [2]], id="column-adjacent"),
        pytest.param([[2], [None], [2]], id="column-separated-by-empty-tiles"),
    ],
)
def test_is_out_of_moves__mergeable__returns_false(board: types.GameBoard):
    assert not board_utils.is_out_of_moves(board)
