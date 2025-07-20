"""Integration tests of file utilities."""

import json
import pathlib
from unittest import mock

import pytest

from python_2048.configurations import exceptions, file_utils


@mock.patch.object(json, "load", autospec=True)
def test_read_game_snapshot(mock_json_load: mock.MagicMock):
    # given:
    file_path = mock.Mock(open=mock.mock_open(), spec_set=pathlib.Path)
    fin = file_path.open.return_value.__enter__.return_value

    # when:
    board = file_utils.read_game_snapshot(file_path)

    # then:
    file_path.open.assert_called_once_with("rb")
    mock_json_load.assert_called_once_with(fin)
    assert board == mock_json_load.return_value


@mock.patch.object(json, "load", autospec=True)
def test_read_game_snapshot__on_io_error__raises_read_error(mock_json_load: mock.MagicMock):
    # given:
    file_path = mock.Mock(spec_set=pathlib.Path)
    file_path.open.side_effect = IOError

    # when:
    with pytest.raises(exceptions.GameSnapshotReadError):
        _ = file_utils.read_game_snapshot(file_path)

    # then:
    file_path.open.assert_called_once_with("rb")
    mock_json_load.assert_not_called()


@mock.patch.object(
    json,
    "load",
    autospec=True,
    side_effect=json.JSONDecodeError("message", "doc", 0),
)
def test_read_game_snapshot__on_json_error__raises_parse_error(mock_json_load: mock.MagicMock):
    # given:
    file_path = mock.Mock(open=mock.mock_open(), spec_set=pathlib.Path)
    fin = file_path.open.return_value.__enter__.return_value

    # when:
    with pytest.raises(exceptions.GameSnapshotParseError):
        _ = file_utils.read_game_snapshot(file_path)

    # then:
    file_path.open.assert_called_once_with("rb")
    mock_json_load.assert_called_once_with(fin)


@mock.patch.object(json, "dump", autospec=True)
def test_try_write_game_snapshot__on_success__returns_true(mock_json_dump: mock.MagicMock):
    # given:
    board = mock.Mock()
    file_path = mock.Mock(open=mock.mock_open(), spec_set=pathlib.Path)
    fout = file_path.open.return_value.__enter__.return_value

    # when:
    succeeded = file_utils.try_write_game_snapshot(board, file_path)

    # then:
    file_path.open.assert_called_once_with("w", encoding="utf-8")
    mock_json_dump.assert_called_once_with(board, fout)
    assert succeeded


@mock.patch.object(json, "dump", autospec=True)
def test_try_write_game_snapshot__on_io_error__returns_false(mock_json_dump: mock.MagicMock):
    # given:
    board = mock.Mock()
    file_path = mock.Mock(spec_set=pathlib.Path)
    file_path.open.side_effect = IOError

    # when:
    succeeded = file_utils.try_write_game_snapshot(board, file_path)

    # then:
    file_path.open.assert_called_once_with("w", encoding="utf-8")
    mock_json_dump.assert_not_called()
    assert not succeeded
