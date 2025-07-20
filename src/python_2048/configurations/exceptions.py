"""Exceptions of configuration utilities."""

import abc
import pathlib


class ConfigurationError(abc.ABC, Exception):
    """A base exception related to configurations."""

    @abc.abstractmethod
    def __str__(self) -> str:
        """A human readable description of the error."""


class GameSnapshotError(ConfigurationError):
    """A base exception related to a game snapshot."""

    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path


class GameSnapshotReadError(GameSnapshotError):
    """Raised when a game snapshot cannot be read."""

    def __str__(self) -> str:
        return f"Failed to read the game snapshot: {self.file_path}"


class GameSnapshotParseError(GameSnapshotError):
    """Raised when a game snapshot cannot be parsed."""

    def __str__(self) -> str:
        return f"Failed to parse the game snapshot: {self.file_path}"
