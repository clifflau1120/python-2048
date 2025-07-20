"""Module that interacts with files."""

import json
import pathlib

from loguru import logger

from python_2048.configurations import exceptions
from python_2048.game import types


def read_game_snapshot(file_path: pathlib.Path) -> types.GameBoard:
    """Read the game board from a previously saved snapshot file.

    Raises:
        GameSnapshotReadError: on failure of file read
        GameSnapshotParseError: on failure of json parse
    """

    try:
        with file_path.open("rb") as fin:
            return json.load(fin)
    except IOError as cause:
        logger.exception("Failed to read the game snapshot: {}", file_path)
        raise exceptions.GameSnapshotReadError(file_path) from cause
    except json.JSONDecodeError as cause:
        logger.exception("Failed to parse the game snapshot: {}", file_path)
        raise exceptions.GameSnapshotParseError(file_path) from cause


def try_write_game_snapshot(board: types.GameBoard, file_path: pathlib.Path) -> bool:
    """
    Write the game board to the `file_path`.

    On I/O error, log a warning and silently return.
    """

    try:
        with file_path.open("w", encoding="utf-8") as fout:
            json.dump(board, fout)
    except IOError:
        logger.warning(
            "Failed to write the game snapshot to: {}",
            file_path,
            exception=True,
        )
        return False
    else:
        logger.info("Wrote the game snapshot to: {}", file_path)
        return True
