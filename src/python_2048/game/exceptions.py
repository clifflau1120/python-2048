"""Module of game-related exceptions."""

import abc

from python_2048.game import types


class GameError(abc.ABC, Exception):
    """A base exception related to the entire game."""

    def __init__(self, board: types.GameBoard):
        self.board = board

    @abc.abstractmethod
    def __str__(self) -> str:
        """A human readable description of the error."""


class GameBoardError(GameError):
    """A base exception related to the game board."""

    def __init__(self, board: types.GameBoard):
        self.board = board


class RowNotExist(GameBoardError):
    def __init__(self, board: types.GameBoard, index: int):
        self.index = index
        super().__init__(board)

    def __str__(self) -> str:
        return f"Expected row {self.index} on the game board."


class ColumnNotAligned(GameBoardError):
    """Raised when one or more columns on a game board have different lengths."""

    def __str__(self) -> str:
        return "Expected all columns on the board has identical lengths."


class InvalidColumnReplacement(GameBoardError):
    """Raised when the board attempts to replace a column with a new one of different length."""

    def __init__(self, board: types.GameBoard, index: int, old_length: int, new_length: int):
        self.index = index
        self.old_length = old_length
        self.new_length = new_length

        super().__init__(board)

    def __str__(self) -> str:
        return (
            f"Cannot replace column {self.index} of length {self.old_length} "
            f"with a new row of length {self.new_length}"
        )
