"""Module of the `run` command."""

import pathlib
import random
import typing

import typer

from python_2048.cli.lib import renderer
from python_2048.configurations import exceptions as configuration_exceptions
from python_2048.configurations import file_utils
from python_2048.game import engine, exceptions, rendering, state
from python_2048.players import human_local, llm

app = typer.Typer()


@app.command()
def run(
    seed: typing.Annotated[
        int | None,
        typer.Option(
            help="An integer that configures the random number generator, "
            "the same seed will always produce the same outcomes.",
        ),
    ] = None,
    silent: typing.Annotated[
        bool,
        typer.Option(
            "-s",
            "--silent",
            help="Whether to suppress UI rendering.",
        ),
    ] = False,
    impersonate: typing.Annotated[
        bool,
        typer.Option(
            "--impersonate",
            help="Whether the `model` would impersonate as the player to play the game.",
        ),
    ] = False,
    model: typing.Annotated[
        str | None,
        typer.Option(
            "-m",
            "--model",
            help="The LLM model identifier, as recognizable by pydantic-ai.",
        ),
    ] = None,
    game_snapshot_path: typing.Annotated[
        pathlib.Path | None,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            show_default="A new game",
            help="The path to a game snapshot.",
        ),
    ] = None,
):
    """Start a new 2048 game."""

    random.seed(seed)

    try:
        board = file_utils.read_game_snapshot(game_snapshot_path) if game_snapshot_path else None
        state_ = state.GameState(board, num_initial_tiles=None)  # random number of initial tiles
        game = engine.GameEngine(state_)
        renderer_ = rendering.DO_NOT_RENDER if silent else renderer.CONSOLE_RENDERER

        assistant = llm.LlmPlayer(model) if model else None

        player = (
            assistant
            if assistant and impersonate
            else human_local.LocalHumanPlayer(assistant=assistant)
        )

        game.start(player, renderer=renderer_)
    except exceptions.GameError:
        print("The game ran into an invalid state, exiting...")
        raise typer.Exit(1)
    except configuration_exceptions.GameSnapshotError:
        print("There is an error in the game snapshot file, exiting...")
        raise typer.Exit(1)
