"""Integration tests for logging setup."""

import pathlib
from unittest import mock

from python_2048.configurations import log_utils


@mock.patch.dict(
    "os.environ",
    {"LOCALAPPDATA": "C:\\Users\\User\\AppData\\Local"},
)
@mock.patch("platform.system", return_value="Windows")
@mock.patch.object(pathlib, "WindowsPath", pathlib.PureWindowsPath)
def test_get_log_directory__windows(_):
    log_directory = log_utils.get_log_directory()
    assert str(log_directory) == "C:\\Users\\User\\AppData\\Local\\python-2048"


@mock.patch.dict(
    "os.environ",
    {"XDG_STATE_HOME": "/home/user/.local/state"},
)
@mock.patch("platform.system", return_value="Linux")
@mock.patch.object(pathlib, "PosixPath", pathlib.PurePosixPath)
def test_get_log_directory__linux(_):
    log_directory = log_utils.get_log_directory()
    assert str(log_directory) == "/home/user/.local/state/python-2048"


@mock.patch.dict("os.environ", {"HOME": "/Users/user"})
@mock.patch("platform.system", return_value="Darwin")
@mock.patch.object(pathlib, "PosixPath", pathlib.PurePosixPath)
def test_get_log_directory__mac_os(_):
    log_directory = log_utils.get_log_directory()
    assert str(log_directory) == "/Users/user/Library/Logs/python-2048"


@mock.patch("os.getcwd")
@mock.patch("os.environ", {})
@mock.patch("platform.system", return_value="Linux")
def test_get_log_directory__missing_env_var__returns_cwd(_, mock_getcwd: mock.MagicMock):
    # given
    cwd = "/home/user/downloads/python-2048"
    mock_getcwd.return_value = cwd

    # when:
    log_directory = log_utils.get_log_directory()

    # then:
    assert str(log_directory) == cwd


@mock.patch("os.getcwd")
@mock.patch("platform.system", return_value="some-unrecognized-system")
def test_get_log_directory__unrecognized_os__returns_cwd(_, mock_getcwd: mock.MagicMock):
    # given
    cwd = "/home/user/downloads/python-2048"
    mock_getcwd.return_value = cwd

    # when:
    log_directory = log_utils.get_log_directory()

    # then:
    assert str(log_directory) == cwd
