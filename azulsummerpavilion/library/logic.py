from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.actions import CompleteInitialization
from azulsummerpavilion.library.actions import DoPlayerTurn
from azulsummerpavilion.library.actions import FillFactoryDisplaySpaces
from azulsummerpavilion.library.actions import FillSupplySpaces
from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.actions import SetGamePhase
from azulsummerpavilion.library.actions import UpdatePlayerScore
from azulsummerpavilion.library.actions import SelectTilesToDrawFromBag
from azulsummerpavilion.library.actions import DistributeTilesToSupply
from azulsummerpavilion.library.constants import PLAYER_TO_DISPLAY_RATIO
from azulsummerpavilion.library.constants import Phase
from azulsummerpavilion.library.constants import INITIAL_PLAYER_SCORE
from azulsummerpavilion.library.constants import SUPPLY_SPACE_COUNT
from azulsummerpavilion.library.events import Event
from azulsummerpavilion.library.events import GameInitialized
from azulsummerpavilion.library.events import GamePhaseSet
from azulsummerpavilion.library.events import PlayerScoreUpdated
from azulsummerpavilion.library.queue import MessageQueue
from azulsummerpavilion.library.state import AzulSummerPavilionState as State


def process_phase_one_action(action: Action, state: State) -> list[Event | None]:
    events = []
    return events


def process_phase_two_action(action: Action, state: State) -> list[Event | None]:
    events = []
    return events


def process_phase_three_action(action: Action, state: State) -> list[Event | None]:
    events = []
    return events


def initialize_game(number_of_players: int) -> State:
    pass


def game_logic(
    action: Action, state: State | None, actions: MessageQueue, events: MessageQueue
) -> (State, MessageQueue, MessageQueue):
    """
    The core game logic to process each tic of the game.

    The logic function takes an action, which contains the game state, and modifies the state.
    The function returns an event which contains a log of the action taken along with the new state.

    The Game class is responsible for processing and emitting actions that require user (player) input or random inputs
    such as selecting tiles to be drawn.
    """
    match action:

        case NewGame(number_of_players=number_of_players):
            actions.append(SetGamePhase(Phase.acquire_tile))
            for player in range(number_of_players):
                actions.append(UpdatePlayerScore(player, INITIAL_PLAYER_SCORE))
            actions.append(FillSupplySpaces())

        case DistributeTilesToSupply():
            # do the distribution
            actions.append(FillFactoryDisplaySpaces())

        case FillFactoryDisplaySpaces():
            for display in range(PLAYER_TO_DISPLAY_RATIO[state.player_count]):
                actions.append()  # specifically target each supply space draw action
            actions.append(CompleteInitialization())

        case UpdatePlayerScore(player=player, score=score):
            state.score.update(player, score)
            events.append(
                PlayerScoreUpdated(
                    player=player,
                    change=score,
                    new_score=state.score.player_score(player),
                )
            )

        case CompleteInitialization():
            state.initializing = False
            actions.append(DoPlayerTurn())

        case SetGamePhase(phase=phase):
            state.phase = phase
            events.append(GamePhaseSet(phase))

        case _:
            pass
    return state, actions, events
