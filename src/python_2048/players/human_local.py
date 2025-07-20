"""Module of `LocalHumanPlayer`."""

import pathlib
import sys

import typer
from rich import print

from python_2048.configurations import file_utils, log_utils
from python_2048.game import types
from python_2048.players import base


class LocalHumanPlayer(base.Player):
    """A human player that plays the game via console."""

    def __init__(self, *, assistant: base.Player | None = None):
        self._assistant = assistant

    def get_next_move(self, board: types.GameBoard) -> types.PlayerDecision:
        while True:
            match option := self._prompt_for_option().lower():
                case (
                    types.SlideDirection.UP
                    | types.SlideDirection.LEFT
                    | types.SlideDirection.DOWN
                    | types.SlideDirection.RIGHT
                ):
                    direction = types.SlideDirection(option)
                    return types.PlayerDecision(direction=direction, reason="")
                case "h":
                    self._ask_for_hint(board)
                case "p":
                    self._save_game(board)
                case "q":
                    self._quit_game()
                case _:
                    print(f"Unrecognized option: {option}")

            print()

    def _ask_for_hint(self, board: types.GameBoard):
        """Ask the `assistant` for hints for the next move."""

        if not self._assistant:
            print("No AI Assistant is configured.")
            return

        suggested_move = self._assistant.get_next_move(board)
        print(f"The AI Assistant suggested: {suggested_move.direction.name}")
        print(f"Reason provided: {suggested_move.reason}")

    @staticmethod
    def _prompt_for_option() -> str:
        """Prompt the user for a single-character option."""

        print("Select an option: ", end="")
        sys.stdout.flush()

        option = typer.getchar(echo=True)
        print()
        print()

        return option

    @staticmethod
    def _save_game(board: types.GameBoard):
        """Prompt the user where to save the current game board."""

        file_path = input("Provide a file path to save the snapshot: ")
        file_path = file_path or "./snapshot.json"
        file_path = pathlib.Path(file_path)

        if file_utils.try_write_game_snapshot(board, file_path):
            print(f"Wrote the game snapshot: {file_path}")
        else:
            print(f"Failed to write the game snapshot: {file_path}")
            print(f"Refer to the application logs: {log_utils.get_log_directory()}")

    @staticmethod
    def _quit_game():
        """Prompt the user if they want to give up."""

        confirmation = input("Are you sure you want to give up (Y/N)? ").strip().upper()
        print()

        if confirmation == "Y":
            print("See you next time!")
            raise typer.Exit(0)
        else:
            print("Let's continue the game!")
