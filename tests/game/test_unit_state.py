"""Unit tests of the `GameState`."""

from unittest import mock

from python_2048.game import state, types
from python_2048.game.lib import board_utils


def test_init__with_board__uses_provided_board():
    # given:
    board: types.GameBoard = [[1, 2, 3]]

    # when:
    game_state = state.GameState(board)

    # then:
    assert game_state.board == board


@mock.patch.object(board_utils, "create_new_board")
def test_init__without_board__creates_new_board(mock_create_new_board: mock.MagicMock):
    # given:
    board: types.GameBoard = [[1, 2, 3]]
    mock_create_new_board.return_value = board

    # when:
    game_state = state.GameState()

    # then:
    assert game_state.board == board


def test_board__mutation__has_no_effect():
    # given:
    board: types.GameBoard = [[1, 2, 3]]
    game_state = state.GameState(board)

    # when:
    game_state.board[0][0] = None

    # then:
    assert game_state.board == [[1, 2, 3]]


@mock.patch.object(board_utils, "get_score")
def test_score(mock_get_score: mock.MagicMock):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    assert game_state.score == mock_get_score.return_value


def test_has_won__when_reached_2048__returns_true():
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    with mock.patch.object(board_utils, "has_2048", return_value=True, autospec=True):
        assert game_state.has_won()


def test_has_won__when_not_reached_2048__returns_false():
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    with mock.patch.object(board_utils, "has_2048", return_value=False, autospec=True):
        assert not game_state.has_won()


def test_is_out_of_moves__returns_true():
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    with mock.patch.object(board_utils, "is_out_of_moves", return_value=True, autospec=True):
        assert game_state.is_out_of_moves()


def test_is_out_of_moves__returns_false():
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    with mock.patch.object(board_utils, "is_out_of_moves", return_value=False, autospec=True):
        assert not game_state.is_out_of_moves()


@mock.patch.object(state.GameState, "slide_up")
def test_slide__upward__calls_slide_up(mock_slide_up: mock.MagicMock):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    succeeded = game_state.slide(types.SlideDirection.UP)

    # then:
    mock_slide_up.assert_called_once()
    assert succeeded == mock_slide_up.return_value


@mock.patch.object(state.GameState, "slide_left")
def test_slide__left_direction__calls_slide_left(mock_slide_left: mock.MagicMock):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    succeeded = game_state.slide(types.SlideDirection.LEFT)

    # then:
    mock_slide_left.assert_called_once()
    assert succeeded == mock_slide_left.return_value


@mock.patch.object(state.GameState, "slide_down")
def test_slide__downward__calls_slide_down(mock_slide_down: mock.MagicMock):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    succeeded = game_state.slide(types.SlideDirection.DOWN)

    # then:
    mock_slide_down.assert_called_once()
    assert succeeded == mock_slide_down.return_value


@mock.patch.object(state.GameState, "slide_right")
def test_slide__right_direction__calls_slide_right(mock_slide_right: mock.MagicMock):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)

    # when:
    succeeded = game_state.slide(types.SlideDirection.RIGHT)

    # then:
    mock_slide_right.assert_called_once()
    assert succeeded == mock_slide_right.return_value


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_up")
def test_slide_up__when_effective__spawns_new_tile(
    mock_move_and_merge_up: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_up.return_value = True

    # when:
    assert game_state.slide_up()

    # then:
    mock_spawn_new_tile.assert_called_once_with(board)


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_up")
def test_slide_up__when_not_effective__does_not_spawn_new_tile(
    mock_move_and_merge_up: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_up.return_value = False

    # when:
    assert not game_state.slide_up()

    # then:
    mock_spawn_new_tile.assert_not_called()


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_left")
def test_slide_left__when_effective__spawns_new_tile(
    mock_move_and_merge_left: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_left.return_value = True

    # when:
    assert game_state.slide_left()

    # then:
    mock_spawn_new_tile.assert_called_once_with(board)


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_left")
def test_slide_left__when_not_effective__does_not_spawn_new_tile(
    mock_move_and_merge_left: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_left.return_value = False

    # when:
    assert not game_state.slide_left()

    # then:
    mock_spawn_new_tile.assert_not_called()


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_down")
def test_slide_down__when_effective__spawns_new_tile(
    mock_move_and_merge_down: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_down.return_value = True

    # when:
    assert game_state.slide_down()

    # then:
    mock_spawn_new_tile.assert_called_once_with(board)


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_down")
def test_slide_down__when_not_effective__does_not_spawn_new_tile(
    mock_move_and_merge_down: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_down.return_value = False

    # when:
    assert not game_state.slide_down()

    # then:
    mock_spawn_new_tile.assert_not_called()


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_right")
def test_slide_right__when_effective__spawns_new_tile(
    mock_move_and_merge_right: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_right.return_value = True

    # when:
    assert game_state.slide_right()

    # then:
    mock_spawn_new_tile.assert_called_once_with(board)


@mock.patch.object(board_utils, "spawn_new_tile")
@mock.patch.object(board_utils, "move_and_merge_right")
def test_slide_right__when_not_effective__does_not_spawn_new_tile(
    mock_move_and_merge_right: mock.MagicMock,
    mock_spawn_new_tile: mock.MagicMock,
):
    # given:
    board = mock.MagicMock()
    game_state = state.GameState(board)
    mock_move_and_merge_right.return_value = False

    # when:
    assert not game_state.slide_right()

    # then:
    mock_spawn_new_tile.assert_not_called()
