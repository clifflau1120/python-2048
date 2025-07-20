"""Module that contains game logic related to tiles."""

import typing

from python_2048.game import exceptions, types


def get_rows(board: types.GameBoard) -> typing.Iterator[tuple[int | None, ...]]:  # pragma: no cover
    """Get all rows from the `board`."""

    for row in board:
        yield tuple(row)


def get_columns(board: types.GameBoard) -> typing.Iterator[tuple[int | None, ...]]:
    """Get all columns from the `board`."""

    try:
        for column in zip(*board, strict=True):
            yield column
    except ValueError as cause:
        raise exceptions.ColumnNotAligned(board) from cause


def replace_row(board: types.GameBoard, new_row: typing.Sequence[int | None], index: int):
    """Replace the specified row on `board` with `new_row`."""

    try:
        board[index] = list(new_row)
    except IndexError as cause:
        raise exceptions.RowNotExist(board, index) from cause


def replace_column(board: types.GameBoard, new_column: typing.Sequence[int | None], index: int):
    """Replace the specified column on `board` with `new_column`."""

    for i in range(len(board)):
        try:
            board[i][index] = new_column[i]
        except IndexError as cause:
            raise exceptions.InvalidColumnReplacement(
                board,
                index,
                old_length=i,
                new_length=len(new_column),
            ) from cause


def move_and_merge_tiles(tiles: typing.Iterable[int | None]) -> tuple[int | None, ...]:
    """
    Move each of the numbers in `tiles` from start to end,
    and merge when two tiles of the same number collide.

    This function is O(n) with a two-pointer approach.
    """

    results = list(tiles)
    left = right = len(results) - 1

    while left >= 0:
        if left == right:
            left -= 1
            continue

        if results[left] is None:
            left -= 1
            continue

        # Move the left tile to the right
        if results[right] is None:
            results[right] = results[left]
            results[left] = None
            left -= 1
            # the right pointer will stay
            # so that it can be merged if there is a same number on the left
            continue

        # Merge the left tile to the right tile
        if results[left] == results[right]:
            results[right] += results[left]  # pyright: ignore[reportOperatorIssue]
            results[left] = None
            left -= 1
            right -= 1
        else:
            right -= 1

    return tuple(results)
