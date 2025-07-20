"""Shared constants of the 2048 game."""

import typing

from python_2048.game import types

DEFAULT_BOARD_SIZE = 4
"""The default size of a `GameBoard`."""

DEFAULT_NUMBER_OF_INITIAL_TILES = 2
"""The default number of initial tiles to be populated on a new `GameBoard`."""

DEFAULT_NEW_TILES: typing.Sequence[types.NewTile] = (
    types.NewTile(value=2, weight=0.9),
    types.NewTile(value=4, weight=0.1),
)
"""A list of 2-tuples, each of which is a potential new tile and its probability to spawn."""
