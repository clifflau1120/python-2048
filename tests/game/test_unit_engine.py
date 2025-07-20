"""Unit tests for the game engine."""

from unittest import mock

from python_2048.game import engine as game_engine
from python_2048.game import rendering
from python_2048.game import state as game_state
from python_2048.players import base as base_player


def test_start__play_until_win__returns_true():
    # given: a transition function to a winning state
    def set_win(state: mock.Mock):
        state.has_won.return_value = True

    # given: a mocked game state
    state = mock.Mock(spec_set=game_state.GameState)
    state.has_won.return_value = False
    state.is_out_of_moves.return_value = False
    state.slide.side_effect = lambda *_: set_win(state)

    # given: a dummy player
    player = mock.Mock(spec_set=base_player.Player)

    # given: a game engine
    game = game_engine.GameEngine(state)

    # when:
    has_won = game.start(player, renderer=rendering.DO_NOT_RENDER)

    # then:
    assert has_won


def test_start__play_until_out_of_moves__returns_false():
    # given: a transition function to a losing state
    def set_lose(state: mock.Mock):
        state.is_out_of_moves.return_value = True

    # given: a mocked game state
    state = mock.Mock(spec_set=game_state.GameState)
    state.has_won.return_value = False
    state.is_out_of_moves.return_value = False
    state.slide.side_effect = lambda *_: set_lose(state)

    # given: a dummy player
    player = mock.Mock(spec_set=base_player.Player)

    # given: a game engine
    game = game_engine.GameEngine(state)

    # when:
    has_won = game.start(player, renderer=rendering.DO_NOT_RENDER)

    # then:
    assert not has_won
