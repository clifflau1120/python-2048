"""LLM evaluations for 2048."""

import pytest

from python_2048.game import types
from python_2048.players import llm

pytestmark = pytest.mark.llm_evaluation


@pytest.mark.parametrize(
    ["model_name"],
    [
        pytest.param("ollama:llama3.1"),
    ],
)
def test_evaluate_get_next_move__suggests_correct_direction(model_name: str):
    # given:
    board = [
        [1024, 1024, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    # when:
    player = llm.LlmPlayer(model_name)
    decision = player.get_next_move(board)

    # then:
    assert decision.direction in {types.SlideDirection.LEFT, types.SlideDirection.RIGHT}
