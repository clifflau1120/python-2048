"""Module that contains game logic related to the board."""

import itertools
import random
import typing

from python_2048.game import constants, types
from python_2048.game.lib import tile_utils


def create_new_board(
    board_size: int = constants.DEFAULT_BOARD_SIZE,
    new_tiles: typing.Sequence[types.NewTile] = constants.DEFAULT_NEW_TILES,
    num_initial_tiles: int | None = constants.DEFAULT_NUMBER_OF_INITIAL_TILES,
) -> types.GameBoard:
    """Create a new 2048 game board, with a number of initial tiles populated.

    Args:
        board_size: the size of each row/column of the game board.
        new_tiles: the content and weights used to spawn new random tiles.
        num_initial_tile: the number of initial tiles populated; evaluates to random if null

    Returns:
        A new game board.
    """

    board = create_empty_board(board_size)

    if num_initial_tiles is None:
        max_initial_tiles = board_size * board_size // 2
        num_initial_tiles = random.randrange(
            min(2, max_initial_tiles),
            max(2, max_initial_tiles) + 1,
        )

    for _ in range(num_initial_tiles):
        spawn_new_tile(board, new_tiles)

    return board


def create_empty_board(board_size: int = constants.DEFAULT_BOARD_SIZE) -> types.GameBoard:
    """Create an empty 2048 game board.

    Args:
        board_size: the size of each row/column of the game board.

    Returns:
        An empty game board.
    """

    return [[None for _ in range(board_size)] for __ in range(board_size)]


def spawn_new_tile(
    board: types.GameBoard,
    new_tiles: typing.Sequence[types.NewTile] = constants.DEFAULT_NEW_TILES,
):
    """Spawn a new tile of 2/4 at a random empty tile on the `board`.

    If there are no empty tiles left, this function returns without spwaning a new tile.

    Args:
        board: the game board where a new tile should be spawned.
        new_tiles: the content and weights used to spawn a new random tile.
    """

    any_empty_tiles = any(tile is None for row in board for tile in row)

    if not any_empty_tiles:
        return

    while True:
        row_index = random.randrange(len(board))
        column_index = random.randrange(len(board[row_index]))

        if board[row_index][column_index] is None:  # pragma: no branch
            new_tile: int = random.choices(*tuple(zip(*new_tiles)))[0]
            board[row_index][column_index] = new_tile
            return


def get_score(board: types.GameBoard) -> int:
    """Calculate the score of the current game board."""

    return sum(filter(None, itertools.chain.from_iterable(board)))


def has_2048(board: types.GameBoard) -> bool:
    """Determine whether there is a tile of 2048."""

    return any(tile == 2048 for tile in itertools.chain.from_iterable(board))


def is_out_of_moves(board: types.GameBoard) -> bool:
    """Determine whether there are no more possible moves on the `board`."""

    def is_moveable(tile_a: int | None, tile_b: int | None) -> bool:
        return (tile_a is None) ^ (tile_b is None)

    def is_mergeable(tile_a: int | None, tile_b: int | None) -> bool:
        return (tile_a is not None) and (tile_b is not None) and (tile_a == tile_b)

    rows = tile_utils.get_rows(board)
    columns = tile_utils.get_columns(board)

    horizontally_adjacent_tile_pairs = itertools.chain.from_iterable(map(itertools.pairwise, rows))
    vertically_adjacent_tile_pairs = itertools.chain.from_iterable(map(itertools.pairwise, columns))

    adjacent_tile_pairs = itertools.chain(
        horizontally_adjacent_tile_pairs,
        vertically_adjacent_tile_pairs,
    )

    return not any(
        is_moveable(*adjacent_tiles) or is_mergeable(*adjacent_tiles)
        for adjacent_tiles in adjacent_tile_pairs
    )


def move_and_merge_up(board: types.GameBoard) -> bool:
    """Move and merge the tiles on board towards upward.

    Args:
        board: the game board

    Returns:
        A boolean that indicates whether there is any effective modification.
    """

    modified = False

    for index, column in enumerate(tile_utils.get_columns(board)):
        new_column = tuple(reversed(tile_utils.move_and_merge_tiles(reversed(column))))

        if column != new_column:
            modified = True
            tile_utils.replace_column(board, new_column, index)

    return modified


def move_and_merge_left(board: types.GameBoard) -> bool:
    """Move and merge the tiles on board towards left.

    Args:
        board: the game board

    Returns:
        A boolean that indicates whether there is any effective modification.
    """

    modified = False

    for index, row in enumerate(tile_utils.get_rows(board)):
        new_row = tuple(reversed(tile_utils.move_and_merge_tiles(reversed(row))))

        if row != new_row:
            modified = True
            tile_utils.replace_row(board, new_row, index)

    return modified


def move_and_merge_down(board: types.GameBoard) -> bool:
    """Move and merge the tiles on board downward.

    Args:
        board: the game board

    Returns:
        A boolean that indicates whether there is any effective modification.
    """

    modified = False

    for index, column in enumerate(tile_utils.get_columns(board)):
        new_column = tile_utils.move_and_merge_tiles(column)

        if column != new_column:
            modified = True
            tile_utils.replace_column(board, new_column, index)

    return modified


def move_and_merge_right(board: types.GameBoard) -> bool:
    """Move and merge the tiles on board towards right.

    Args:
        board: the game board

    Returns:
        A boolean that indicates whether there is any effective modification.
    """

    modified = False

    for index, row in enumerate(tile_utils.get_rows(board)):
        new_row = tile_utils.move_and_merge_tiles(row)

        if row != new_row:
            modified = True
            tile_utils.replace_row(board, new_row, index)

    return modified
