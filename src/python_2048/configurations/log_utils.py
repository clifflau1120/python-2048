"""Module that sets up logging."""

import logging
import os
import pathlib
import platform

from loguru import logger

from python_2048.version import __app__

_LOG_FORMAT = " | ".join(
    (
        "'<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>",
        "<level>{level: <8}</level>",
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
        "<level>{message}</level>",
        "{extra}",
    )
)


def remove_default_sink():  # pragma: no cover
    """Remove the default sink."""

    logger.remove()


def add_file_as_sink(level: int = logging.INFO):  # pragma: no cover
    """Set up file logging with rotation."""

    log_directory = get_log_directory().absolute()

    try:
        log_directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    except OSError:
        logger.warning(
            "Failed to create the log directory, no log files will be produced: {}",
            log_directory,
            exception=True,
        )
    else:
        logger.add(log_directory / "{time}.log", level=level, colorize=True, format=_LOG_FORMAT)


def get_log_directory() -> pathlib.Path:
    """Determine the log directory based on the operating system."""

    try:
        match system_name := platform.system():
            case "Windows":
                return pathlib.WindowsPath(os.environ["LOCALAPPDATA"], __app__)
            case "Linux":
                return pathlib.PosixPath(os.environ["XDG_STATE_HOME"], __app__)
            case "Darwin":
                return pathlib.PosixPath(os.environ["HOME"], "Library", "Logs", __app__)
            case _:
                logger.warning(
                    "Failed to determine a log directory for unrecognized operating system {}, "
                    "falling back to the current directory.",
                    system_name,
                    exception=True,
                )
    except KeyError as cause:
        logger.warning(
            "Failed to determine a log directory from a missing environment variable: {}",
            cause.args[0],
            exception=True,
        )

    return pathlib.Path(os.getcwd())
