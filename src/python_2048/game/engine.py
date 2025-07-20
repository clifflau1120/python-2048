"""Module of `GameEngine`."""

from python_2048.game import rendering, state
from python_2048.players import base


class GameEngine:
    """The game engine of 2048."""

    def __init__(self, state_: state.GameState | None = None):
        self._state = state_ or state.GameState()

    def start(self, player: base.Player, *, renderer: rendering.GameRenderingProtocol) -> bool:
        """Start the game loop, until a win/lose is determined.

        Args:
            player: the input source to get next moves from.
            renderer: the ui renderer to call on certain game states.

        Returns:
            `True` if the player wins the game, `False` otherwise.
        """

        renderer.on_init()

        while True:
            renderer.on_start(self._state.board)

            if self._state.has_won():
                renderer.on_win()
                return True

            if self._state.is_out_of_moves():
                renderer.on_lose()
                return False

            renderer.before_next_move()

            player_move = player.get_next_move(self._state.board)

            renderer.after_next_move(player_move)

            self._state.slide(player_move.direction)
