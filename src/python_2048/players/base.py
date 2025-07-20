"""Module of `Player`."""

import abc

from python_2048.game import types


class Player(abc.ABC):
    """A `Player` represents a source of `PlayerDecision`."""

    @abc.abstractmethod
    def get_next_move(self, board: types.GameBoard) -> types.PlayerDecision:
        """Get the next move from the player.

        Args:
            board: the 2048 game board.

        Returns:
            The player's decision based on the given `board`.
        """
