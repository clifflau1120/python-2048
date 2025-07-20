"""Integration tests for `LlmPlayer`."""

import json
from unittest import mock

import pydantic_ai
import pydantic_ai.exceptions
import pydantic_ai.models.openai
import pydantic_ai.providers.openai
import pytest

from python_2048.game import types
from python_2048.players import exceptions, llm

MOCK_MODEL_NAME = "some-llm-model"


@mock.patch.object(pydantic_ai, "Agent")
@mock.patch.object(pydantic_ai.models.openai, "OpenAIModel")
@mock.patch.object(pydantic_ai.providers.openai, "OpenAIProvider")
def test_init__recognizes_ollama_model(
    mock_ollama_provider_cls: mock.MagicMock,
    mock_ollama_model_cls: mock.MagicMock,
    mock_agent_cls: mock.MagicMock,
):
    # given:
    mock_ollama_model = mock_ollama_model_cls.return_value
    mock_ollama_provider = mock_ollama_provider_cls.return_value
    # when:
    _ = llm.LlmPlayer(f"ollama:{MOCK_MODEL_NAME}")

    # then: an ollama provider is constructed
    mock_ollama_provider_cls.assert_called_once_with(base_url=llm.DEFAULT_OLLAMA_HOST)

    # then: an ollama model with only the model name is constructed
    mock_ollama_model_cls.assert_called_once_with(MOCK_MODEL_NAME, provider=mock_ollama_provider)

    # then: the agent should use the ollama model
    mock_agent_cls.assert_called_once()
    assert mock_agent_cls.call_args.args[0] == mock_ollama_model


def test_init__unknown_model__raises_llm_exception():
    with pytest.raises(exceptions.LlmException):
        _ = llm.LlmPlayer("some-unknown-model")


@mock.patch.object(pydantic_ai, "Agent")
@mock.patch.object(json, "dumps")
def test_get_next_move(mock_json_dumps: mock.MagicMock, mock_agent_cls: mock.MagicMock):
    # given:
    board = mock.Mock()
    serialized_board = mock_json_dumps.return_value

    agent = mock_agent_cls.return_value
    agent.run_sync.return_value.output = types.PlayerDecision(
        direction=types.SlideDirection.RIGHT,
        reason="Slide to right to maximize tile values and organize the board.",
    )

    llm_player = llm.LlmPlayer(MOCK_MODEL_NAME)

    # when:
    decision = llm_player.get_next_move(board)

    # then:
    mock_json_dumps.assert_called_once_with(board)
    agent.run_sync.assert_called_once_with(serialized_board)
    assert decision.direction == types.SlideDirection.RIGHT


@mock.patch.object(pydantic_ai, "Agent")
@mock.patch.object(json, "dumps")
def test_get_next_move__unexpected_model_behavior__raises_llm_exception(
    _,
    mock_agent_cls: mock.MagicMock,
):
    # given:
    board = mock.Mock()

    agent = mock_agent_cls.return_value
    agent.run_sync.side_effect = pydantic_ai.exceptions.UnexpectedModelBehavior("act weird")

    llm_player = llm.LlmPlayer(MOCK_MODEL_NAME)

    # when:
    with pytest.raises(exceptions.LlmException):
        _ = llm_player.get_next_move(board)
