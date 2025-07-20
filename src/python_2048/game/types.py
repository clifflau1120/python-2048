"""Type definitions of the 2048 game."""

import enum
import typing

import pydantic

GameBoard = list[list[int | None]]
"""A 2d-matrix representation of the game board."""


class NewTile(typing.NamedTuple):
    """A new tile that can be spawned in a game board."""

    value: int
    """The numeric value of the new tile."""

    weight: float
    """The weight of `value` in the random sampling."""


class SlideDirection(str, enum.Enum):
    """An enumeration of slide directions towards which tiles are moved and merged."""

    UP = "w"
    LEFT = "a"
    DOWN = "s"
    RIGHT = "d"


class PlayerDecision(pydantic.BaseModel):
    direction: SlideDirection
    """The direction that a player decides."""

    reason: str
    """The reason why the player picks the direction."""
