"""Module that exposes console-based game rendering utilities."""

import rich
import rich.table
import tabulate

from python_2048.game import types
from python_2048.game.lib import board_utils

_BANNER = """
░▒▓███████▓▒░ ░▒▓████████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓██████▓▒░
       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓████████▓▒░ ░▒▓██████▓▒░
░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
░▒▓████████▓▒░░▒▓████████▓▒░       ░▒▓█▓▒░ ░▒▓██████▓▒░
"""

_RULES = """
1. [bold]Game board[/bold]: The game is played on 4x4 grid by default.
2. [bold]Tiles[/bold]: Each tile on the game board can be empty, or filled with a number.
3. [bold]Starting tiles[/bold]: At the beginning of the game, a random number of 2/4 are placed on the board.
4. [bold]Sliding tiles[/bold]: The player can slide tiles in four directions (up, left, down, right), denoted by WASD.
5. [bold]Merging tiles[/bold]: When two tiles of the same number collide during a slide, they merge into a single tile with the sum.
6. [bold]Spawning tiles[/bold]: Each time the player makes a move, a new tile of 2/4 is spawned on the board.
7. [bold]How to win[/bold]: The goal is to have a tile with the number 2048.
8. [bold]Game over[/bold]: The game ends when the board is full and no further moves are possible.
"""


console = rich.console.Console()


def print_introduction():
    """Print an introduction to the game."""

    console.print(_BANNER, highlight=False)
    console.print("--------------- Welcome to the 2048 Game ----------------")
    console.print(_RULES, highlight=False)
    console.print("-------------------- Enjoy the Game ! --------------------")
    console.print()


def print_board_and_score(board: types.GameBoard):
    """Print the board and the latest score on screen."""

    console.print(tabulate.tabulate(board, tablefmt="rounded_grid"), highlight=False)
    console.print()
    console.print(f"[bold]Score[/bold]: {board_utils.get_score(board)}")
    console.print()


def print_user_manual():
    """Print the user manual."""

    table = rich.table.Table()

    table.add_column("Keystroke", style="cyan")
    table.add_column("Description", style="magenta")

    table.add_row(types.SlideDirection.UP, "Slide up")
    table.add_row(types.SlideDirection.LEFT, "Slide left")
    table.add_row(types.SlideDirection.DOWN, "Slide down")
    table.add_row(types.SlideDirection.RIGHT, "Slide right")
    table.add_row("h", "Get AI Suggestion")
    table.add_row("p", "Save the game")
    table.add_row("q", "Give up")

    console.print(table)


def print_player_decision(decision: types.PlayerDecision):
    """Print a prompt for the player's next move."""

    console.print(f"You selected: {decision.direction.name}")

    if decision.reason:
        console.print(f"Reason provided: {decision.reason}")

    console.print()


def print_win_message():
    """Congratulate the player for winning the game."""

    console.print("Congratulations, you win!")


def print_lose_message():
    """Congratulate the player for losing the game."""

    console.print("Game over!")
