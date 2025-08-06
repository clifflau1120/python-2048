"""Module of the `run` command."""

import pathlib
import random
import typing

import pydantic_ai.providers
import typer
from pydantic_ai.models import openai

from python_2048.cli.lib import renderer
from python_2048.configurations import exceptions as configuration_exceptions
from python_2048.configurations import file_utils
from python_2048.game import engine, exceptions, rendering, state
from python_2048.players import human_local, llm

OLLAMA_PROVIDER = "openai"
OLLAMA_LOCAL_BASE_URL = "http://localhost:11434/v1"


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
    base_url: typing.Annotated[
        str,
        typer.Option(
            "-u",
            "--base-url",
            help="The base url of the LLM provider.",
        ),
    ] = OLLAMA_LOCAL_BASE_URL,
    provider_name: typing.Annotated[
        str | None,
        typer.Option(
            "-p",
            "--provider",
            help="The LLM provider, as recognizable by pydantic-ai.",
        ),
    ] = OLLAMA_PROVIDER,
    model_name: typing.Annotated[
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

        provider = (
            pydantic_ai.providers.infer_provider_class(provider_name)(base_url=base_url)  # type: ignore
            if provider_name
            else None
        )

        model = (
            openai.OpenAIModel(model_name, provider=provider) if model_name and provider else None
        )

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
