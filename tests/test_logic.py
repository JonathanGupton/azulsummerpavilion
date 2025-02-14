from unittest.mock import MagicMock
from unittest.mock import patch

from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.components.constants import Phase
from azulsummerpavilion.library.components.state import AzulSummerPavilionState as State
from azulsummerpavilion.library.logic.logic import game_logic
from azulsummerpavilion.library.queue import MessageDequeue


@patch("azulsummerpavilion.library.logic.logic.game_start")
def test_game_logic_calls_game_start_when_no_phase_and_game_not_ended(mock_game_start):
    action = MagicMock(spec=Action)
    state = MagicMock(spec=State)
    state.game_end = False
    state.phase = None
    aq = MessageDequeue()
    eq = MessageDequeue()

    game_logic(action, state, aq, eq)

    mock_game_start.assert_called_once_with(action, state, aq, eq)


@patch("azulsummerpavilion.library.logic.logic.phase_one")
def test_game_logic_calls_phase_one_when_in_acquire_tile_phase(mock_phase_one):
    action = MagicMock(spec=Action)
    state = MagicMock(spec=State)
    state.phase = Phase.acquire_tile
    aq = MessageDequeue()
    eq = MessageDequeue()

    game_logic(action, state, aq, eq)

    mock_phase_one.assert_called_once_with(action, state, aq, eq)


@patch("azulsummerpavilion.library.logic.logic.phase_two")
def test_game_logic_calls_phase_two_when_in_play_tile_phase(mock_phase_two):
    action = MagicMock(spec=Action)
    state = MagicMock(spec=State)
    state.phase = Phase.play_tiles
    aq = MessageDequeue()
    eq = MessageDequeue()

    game_logic(action, state, aq, eq)

    mock_phase_two.assert_called_once_with(action, state, aq, eq)


@patch("azulsummerpavilion.library.logic.logic.phase_three")
def test_game_logic_calls_phase_three_when_in_prep_next_round_phase(mock_phase_three):
    action = MagicMock(spec=Action)
    state = MagicMock(spec=State)
    state.phase = Phase.prepare_next_round
    aq = MessageDequeue()
    eq = MessageDequeue()

    game_logic(action, state, aq, eq)

    mock_phase_three.assert_called_once_with(action, state, aq, eq)


@patch("azulsummerpavilion.library.logic.logic.game_end")
def test_game_logic_calls_game_end_when_no_phase_and_game_ended(mock_game_end):
    action = MagicMock(spec=Action)
    state = MagicMock(spec=State)
    state.phase = None
    state.game_end = True
    aq = MessageDequeue()
    eq = MessageDequeue()

    game_logic(action, state, aq, eq)

    mock_game_end.assert_called_once_with(action, state, aq, eq)
