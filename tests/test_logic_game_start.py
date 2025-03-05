import pytest

from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.actions import FillSupplySpaces
from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.actions import SetGamePhase
from azulsummerpavilion.library.actions import SetRoundAndWildColor
from azulsummerpavilion.library.actions import UpdatePlayerScore
from azulsummerpavilion.library.components.color import Purple
from azulsummerpavilion.library.components.constants import INITIAL_PLAYER_SCORE
from azulsummerpavilion.library.components.constants import Phase
from azulsummerpavilion.library.logic.game_start import game_start
from azulsummerpavilion.library.queue import MessageDequeue


@pytest.fixture
def action_queue():
    return MessageDequeue()


@pytest.fixture
def event_queue():
    return MessageDequeue()


def test_new_game_two_players(action_queue, event_queue):
    # When
    game_start(NewGame(2), None, action_queue, event_queue)

    # Then
    expected_actions = [
        SetRoundAndWildColor(game_round=1, wild_color=Purple()),
        UpdatePlayerScore(0, INITIAL_PLAYER_SCORE),
        UpdatePlayerScore(1, INITIAL_PLAYER_SCORE),
        FillSupplySpaces(),
        SetGamePhase(Phase.acquire_tile),
    ]

    assert len(action_queue) == 5
    for expected, actual in zip(expected_actions, action_queue):
        assert type(expected) == type(actual)
        assert expected.__dict__ == actual.__dict__


def test_new_game_four_players(action_queue, event_queue):
    # When
    game_start(NewGame(4), None, action_queue, event_queue)

    # Then
    expected_actions = [
        SetRoundAndWildColor(game_round=1, wild_color=Purple()),
        UpdatePlayerScore(0, INITIAL_PLAYER_SCORE),
        UpdatePlayerScore(1, INITIAL_PLAYER_SCORE),
        UpdatePlayerScore(2, INITIAL_PLAYER_SCORE),
        UpdatePlayerScore(3, INITIAL_PLAYER_SCORE),
        FillSupplySpaces(),
        SetGamePhase(Phase.acquire_tile),
    ]

    assert len(action_queue) == 7
    for expected, actual in zip(expected_actions, action_queue):
        assert type(expected) == type(actual)
        assert expected.__dict__ == actual.__dict__


def test_phase_one_set_round_and_wild_color(action_queue, event_queue, mocker):
    # Given
    handle_mock = mocker.patch(
        "azulsummerpavilion.library.logic.game_start.handle_set_round_and_wild_color"
    )
    action = SetRoundAndWildColor(game_round=2, wild_color=Purple())

    # When
    game_start(action, None, action_queue, event_queue)

    # Then
    handle_mock.assert_called_once_with(game_state, 2, Purple())
    assert len(action_queue) == 0


def test_phase_one_unhandled_action(
    action_queue, event_queue, game_start_state_2_players
):
    # Given

    class UnhandledAction(Action):
        pass

    action = UnhandledAction()

    game_start(action, game_start_state_2_players, action_queue, event_queue)

    assert len(action_queue) == 0


def test_phase_one_new_game_invalid_player_count(action_queue, event_queue, game_state):
    # When/Then
    for invalid_count in [-1, 0, 5, 10]:
        game_start(NewGame(invalid_count), game_state, action_queue, event_queue)

        # Verify initial actions are still created
        assert isinstance(action_queue.popleft(), SetRoundAndWildColor)
        action_queue.actions.clear()
