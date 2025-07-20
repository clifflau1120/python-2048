"""Module of `GameRenderingProtocol`."""

import typing

from python_2048.game import types


class GameRenderingProtocol(typing.NamedTuple):
    """Defines a protocol that renders the game ui."""

    on_init: typing.Callable[[], None]
    """Called on the initialization of the game."""

    on_start: typing.Callable[[types.GameBoard], None]
    """Called on the start of each game loop."""

    before_next_move: typing.Callable[[], None]
    """Called just before the player makes the next move."""

    after_next_move: typing.Callable[[types.PlayerDecision], None]
    """Called right after the player makes the next move."""

    on_win: typing.Callable[[], None]
    """Called on winning the game."""

    on_lose: typing.Callable[[], None]
    """Called on losing the game."""


def _do_nothing(*_, **__):
    pass


DO_NOT_RENDER = GameRenderingProtocol(
    on_init=_do_nothing,
    on_start=_do_nothing,
    before_next_move=_do_nothing,
    after_next_move=_do_nothing,
    on_win=_do_nothing,
    on_lose=_do_nothing,
)
"""Signify that the game does not need UI rendering."""
