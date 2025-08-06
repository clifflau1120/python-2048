"""LLM evaluations for 2048."""

import pydantic_ai.providers
import pytest
from pydantic_ai.models import openai

from python_2048.game import types
from python_2048.players import llm

pytestmark = pytest.mark.llm_evaluation

OLLAMA_PROVIDER = "openai"
OLLAMA_LOCAL_BASE_URL = "http://localhost:11434/v1"


@pytest.mark.parametrize(
    ["model_name", "provider_name", "base_url"],
    [
        pytest.param("llama3.1", OLLAMA_PROVIDER, OLLAMA_LOCAL_BASE_URL, id="ollama:llama3.1"),
    ],
)
def test_evaluate_get_next_move__suggests_correct_direction(
    model_name: str, provider_name: str, base_url: str
):
    # given:
    board = [
        [1024, 1024, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    provider = pydantic_ai.providers.infer_provider_class(provider_name)(base_url=base_url)  # type: ignore
    model = openai.OpenAIModel(model_name, provider=provider)

    # when:
    player = llm.LlmPlayer(model)
    decision = player.get_next_move(board)

    # then:
    assert decision.direction in {types.SlideDirection.LEFT, types.SlideDirection.RIGHT}
