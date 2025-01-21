from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.actions import CompleteInitialization
from azulsummerpavilion.library.actions import DistributeTiles
from azulsummerpavilion.library.actions import DoPlayerTurn
from azulsummerpavilion.library.actions import FillFactoryDisplaySpaces
from azulsummerpavilion.library.actions import FillSupplySpaces
from azulsummerpavilion.library.actions import MakeTileSelection
from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.actions import SetGamePhase
from azulsummerpavilion.library.actions import SetRoundAndWildColor
from azulsummerpavilion.library.actions import UpdatePlayerScore
from azulsummerpavilion.library.constants import Bag
from azulsummerpavilion.library.constants import FACTORY_SPACE_DRAW
from azulsummerpavilion.library.constants import FactoryDisplay
from azulsummerpavilion.library.constants import INITIAL_PLAYER_SCORE
from azulsummerpavilion.library.constants import PLAYER_TO_DISPLAY_RATIO
from azulsummerpavilion.library.constants import Phase
from azulsummerpavilion.library.constants import Purple
from azulsummerpavilion.library.constants import SUPPLY_SPACE_COUNT
from azulsummerpavilion.library.constants import Supply
from azulsummerpavilion.library.events import GamePhaseSet
from azulsummerpavilion.library.events import PlayerScoreUpdated
from azulsummerpavilion.library.queue import MessageQueue
from azulsummerpavilion.library.state import AzulSummerPavilionState as State


def game_logic(
    action: Action, state: State | None, aq: MessageQueue, eq: MessageQueue
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
            aq.append(SetGamePhase(Phase.acquire_tile))
            aq.append(SetRoundAndWildColor(game_round=1, wild_color=Purple()))
            for player in range(number_of_players):
                aq.append(UpdatePlayerScore(player, INITIAL_PLAYER_SCORE))
            aq.append(FillSupplySpaces())  # Handled by GM

        case FillSupplySpaces():
            aq.appendleft(
                MakeTileSelection(
                    tile_count=SUPPLY_SPACE_COUNT, source=Bag(), target=Supply()
                )
            )

        case FillFactoryDisplaySpaces():
            number_of_displays = PLAYER_TO_DISPLAY_RATIO[state.player_count]
            for display_index in reversed(range(number_of_displays)):
                aq.appendleft(
                    MakeTileSelection(
                        tile_count=FACTORY_SPACE_DRAW,
                        source=Bag(),
                        target=FactoryDisplay(display_index),
                    )
                )
            aq.append(CompleteInitialization())

        case DistributeTiles(tiles=tiles, source=source, target=target) if isinstance(
            target, Supply
        ):

            # TODO:  do the distribution
            aq.append(FillFactoryDisplaySpaces())

        case DistributeTiles(tiles=tiles, source=source, target=target) if isinstance(
            target, FactoryDisplay
        ):
            display_index = target.display_index

        case UpdatePlayerScore(player=player, score=score):
            state.score.update(player, score)
            eq.append(
                PlayerScoreUpdated(
                    player=player,
                    change=score,
                    new_score=state.score.player_score(player),
                )
            )

        case CompleteInitialization():
            state.initializing = False
            aq.append(DoPlayerTurn())

        case SetGamePhase(phase=phase):
            state.phase = phase
            eq.append(GamePhaseSet(phase))

        case SetRoundAndWildColor(game_round=game_round, wild_color=wild_color):
            state.round = game_round
            state.wild_color = wild_color

        case _:
            pass
    return state, aq, eq
