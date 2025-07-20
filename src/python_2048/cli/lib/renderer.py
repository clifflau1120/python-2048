"""Module that exposes a console-based Game UI Renderer."""

from python_2048.cli.lib import rendering as cli_rendering
from python_2048.game import rendering

CONSOLE_RENDERER = rendering.GameRenderingProtocol(
    on_init=cli_rendering.print_introduction,
    on_start=cli_rendering.print_board_and_score,
    before_next_move=cli_rendering.print_user_manual,
    after_next_move=cli_rendering.print_player_decision,
    on_win=cli_rendering.print_win_message,
    on_lose=cli_rendering.print_lose_message,
)
"""Render the Game UI on console."""
