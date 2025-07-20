"""Module of `GameState`."""

import copy

import typing_extensions

from python_2048.game import constants, types
from python_2048.game.lib import board_utils


class GameState:
    """A public interface to mutate and manage the game state of 2048."""

    def __init__(
        self,
        board: types.GameBoard | None = None,
        num_initial_tiles: int | None = constants.DEFAULT_NUMBER_OF_INITIAL_TILES,
    ):
        """
        Args:
            board: a game board configuration, where a new one would be created if null
            num_initial_tiles: if a new board is being created, the number of initial tiles
                to be populated; evaluates to a random number if null.
        """

        self._board = board or board_utils.create_new_board(num_initial_tiles=num_initial_tiles)

    @property
    def board(self) -> types.GameBoard:
        """The game board."""

        return copy.deepcopy(self._board)  # prevent unexpected mutations

    @property
    def score(self) -> int:
        """The current score of the game."""

        return board_utils.get_score(self._board)

    def has_won(self) -> bool:
        """Whether the player has won the game."""

        return board_utils.has_2048(self._board)

    def is_out_of_moves(self) -> bool:
        """Whether the player has lost the game."""

        return board_utils.is_out_of_moves(self._board)

    def slide(self, direction: types.SlideDirection) -> bool:
        """
        Slide the tiles to a provided `direction`,
        then spawn a new tile if it is an effective move.
        """

        match direction:
            case types.SlideDirection.UP:
                return self.slide_up()
            case types.SlideDirection.LEFT:
                return self.slide_left()
            case types.SlideDirection.DOWN:
                return self.slide_down()
            case types.SlideDirection.RIGHT:
                return self.slide_right()
            case _:  # pragma: no cover
                typing_extensions.assert_never()

    def slide_up(self) -> bool:
        """Slide the tiles to the top, then spawn a new tile if it is an effective move."""

        if board_utils.move_and_merge_up(self._board):
            board_utils.spawn_new_tile(self._board)
            return True

        return False

    def slide_left(self) -> bool:
        """Slide the tiles to the left, then spawn a new tile if it is an effective move."""

        if board_utils.move_and_merge_left(self._board):
            board_utils.spawn_new_tile(self._board)
            return True

        return False

    def slide_down(self) -> bool:
        """Slide the tiles to the bottom, then spawn a new tile if it is an effective move."""

        if board_utils.move_and_merge_down(self._board):
            board_utils.spawn_new_tile(self._board)
            return True

        return False

    def slide_right(self) -> bool:
        """Slide the tiles to the right, then spawn a new tile if it is an effective move."""

        if board_utils.move_and_merge_right(self._board):
            board_utils.spawn_new_tile(self._board)
            return True

        return False
