"""Integration tests for `LlmPlayer`."""

import json
from unittest import mock

import pydantic_ai
import pydantic_ai.exceptions
import pydantic_ai.models
import pydantic_ai.models.openai
import pydantic_ai.providers.openai
import pytest

from python_2048.game import types
from python_2048.players import exceptions, llm


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

    model = mock.Mock(spec_set=pydantic_ai.models.Model)
    llm_player = llm.LlmPlayer(model)

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

    model = mock.Mock(spec_set=pydantic_ai.models.Model)
    llm_player = llm.LlmPlayer(model)

    # when:
    with pytest.raises(exceptions.LlmException):
        _ = llm_player.get_next_move(board)
