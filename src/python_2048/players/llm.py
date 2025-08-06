"""Module of `LlmPlayer`."""

import json

import pydantic_ai
import pydantic_ai.exceptions
import pydantic_ai.models

from python_2048.game import types
from python_2048.players import base, exceptions

_SYSTEM_PROMPT = """
You are an expert player of the game 2048.

Your goal is to analyze the provided 2048 game board and suggest a single most optimal move, along with a short reason in one sentence.

<game_rules>
- Game board: this game is played on an M by N grid.
- Tile: each tile on the game board can either be empty, or with a number.
- Tile Movement: player can slide tiles in four directions (up, left, down, right), denoted by wasd.
- Tile Merging: when two tiles with the same number collide during a move, they merge into a single tile with the sum of both parent tiles.
- Invalid movement: if a direction cannot produce any actual movement or mergeing of tiles, the movement is considered invalid.
- New Tile Spawn: after each grid move, a new tile of either 2 or 4 is spawned in a random empty tile on the board.
- Winning: the game is won when a tile with the number 2048 is created.
- Game over: the game ends when the board is full, and no further moves are possible.
</game_rules>

<board_representation>
The board is represented as 2-dimensional JSON arrays.
board[x][y] represents a tile at row x, column y.
</board_representation>

<optimal_move>
The goal of the game is to create a tile with the number 2048.
It can be achieved by the following sub-objectives:
1. Maximize merges: prioritize moves that create higher-value tiles
2. Keep high-value tiles in corners/edges: keep the board organized and prevent blocking
3. Maintain an open board: avoid moves that rapidly fill the board, limiting future options
4. Setting up future merges: looking ahead more than one move
5. Avoid death traps: situations where no further merges are possible
</optimal_move>
"""


class LlmPlayer(base.Player):
    """A Large Language Model that impersonates as a player."""

    def __init__(self, model: pydantic_ai.models.Model):
        try:
            self._agent = pydantic_ai.Agent(
                model,
                system_prompt=_SYSTEM_PROMPT,
                output_type=types.PlayerDecision,
            )
        except pydantic_ai.exceptions.UserError as cause:  # pragma: no cover
            raise exceptions.LlmException(model) from cause

    def get_next_move(self, board: types.GameBoard) -> types.PlayerDecision:
        user_prompt = json.dumps(board)

        try:
            result = self._agent.run_sync(user_prompt)
        except pydantic_ai.exceptions.UnexpectedModelBehavior as cause:
            raise exceptions.LlmException(self._agent.model) from cause

        return result.output
