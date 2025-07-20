"""Unit tests for the game logic related to tiles."""

import typing

import pytest

from python_2048.game import exceptions, types
from python_2048.game.lib import tile_utils


@pytest.mark.parametrize(
    ["board", "expected"],
    [
        pytest.param([], [], id="empty-board"),
        pytest.param(
            [
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
            ],
            [
                (1, 1, 1, 1),
                (2, 2, 2, 2),
                (3, 3, 3, 3),
                (4, 4, 4, 4),
            ],
            id="square-board",
        ),
        pytest.param(
            [
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
                [5, 4, 3, 2, 1],
                [5, 4, 3, 2, 1],
            ],
            [
                (1, 1, 5, 5),
                (2, 2, 4, 4),
                (3, 3, 3, 3),
                (4, 4, 2, 2),
                (5, 5, 1, 1),
            ],
            id="rectangular-board",
        ),
    ],
)
def test_get_columns(board: types.GameBoard, expected: list[tuple[int | None, ...]]):
    columns = list(tile_utils.get_columns(board))
    assert columns == expected


def test_get_columns__irregular_board__raises_column_not_aligned():
    board: types.GameBoard = [
        [1, 2, 3, 4],
        [1, 2, 3],
        [1, 2],
        [1],
    ]

    with pytest.raises(exceptions.ColumnNotAligned):
        _ = list(tile_utils.get_columns(board))


def test_replace_row():
    # given:
    board: types.GameBoard = [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]

    new_row = [4, 3, 2, 1]

    # when:
    tile_utils.replace_row(board, new_row, index=2)

    # then:
    assert board == [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [1, 2, 3, 4],
    ]


def test_replace_row__do_not_exist():
    # given:
    board: types.GameBoard = [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]

    new_row = [4, 3, 2, 1]

    # when:
    with pytest.raises(exceptions.RowNotExist) as exc_info:
        tile_utils.replace_row(board, new_row, index=5)

    # then:
    assert exc_info.value.index == 5


def test_replace_column():
    # given:
    board: types.GameBoard = [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]

    new_column = [6, 7, 8, 9]

    # when:
    tile_utils.replace_column(board, new_column, index=2)

    # then:
    assert board == [
        [1, 2, 6, 4],
        [1, 2, 7, 4],
        [1, 2, 8, 4],
        [1, 2, 9, 4],
    ]


def test_replace_column__irregular_board__raises_invalid_replacement():
    # given:
    board: types.GameBoard = [
        [1, 2, 3, 4],
        [1, 2],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]

    new_column = [6, 7, 8, 9]

    # when:
    with pytest.raises(exceptions.InvalidColumnReplacement) as exc_info:
        tile_utils.replace_column(board, new_column, index=2)

    # then:
    assert exc_info.value.index == 2
    assert exc_info.value.old_length == 1
    assert exc_info.value.new_length == 4


@pytest.mark.parametrize(
    ["tiles", "expected"],
    [
        pytest.param((), (), id="empty-board"),
        pytest.param((None, None, None, None), (None, None, None, None), id="no-tiles"),
        pytest.param((2, None, None, 4), (None, None, 2, 4), id="move-tiles-no-merge"),
        pytest.param((None, None, 2, 2), (None, None, None, 4), id="merge-tiles-no-move-single"),
        pytest.param((2, 2, 2, 2), (None, None, 4, 4), id="merge-tiles-no-move-multiple"),
        pytest.param((2, None, 2, 2), (None, None, 2, 4), id="move-and-merge-tiles"),
        pytest.param((2, 4, 2, 4), (2, 4, 2, 4), id="no-move-and-merge"),
    ],
)
def test_move_and_merge_tiles(tiles: typing.Iterable[int | None], expected: tuple[int | None, ...]):
    assert tile_utils.move_and_merge_tiles(tiles) == expected
