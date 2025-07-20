"""Exceptions for player operations."""

import abc

import pydantic_ai.models


class PlayerException(abc.ABC, Exception):
    """A base exception for player operations."""

    @abc.abstractmethod
    def __str__(self) -> str:
        """A human readable description of the error."""


class LlmException(PlayerException):
    """Raised when `pydantic-ai` fails to interact with the LLM."""

    def __init__(self, model: str | pydantic_ai.models.Model | None):
        self.model = model

    def __str__(self) -> str:
        return f"Failed to interact with the LLM: {self.model}"
