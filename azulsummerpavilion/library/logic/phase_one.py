import inspect

from loguru import logger

from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.actions import FillSupplySpaces
from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.actions import SetGamePhase
from azulsummerpavilion.library.actions import SetRoundAndWildColor
from azulsummerpavilion.library.actions import UpdatePlayerScore
from azulsummerpavilion.library.components.color import Purple
from azulsummerpavilion.library.components.constants import INITIAL_PLAYER_SCORE
from azulsummerpavilion.library.components.constants import Phase
from azulsummerpavilion.library.components.state import AzulSummerPavilionState as State
from azulsummerpavilion.library.queue import MessageQueue


def handle_new_game(number_of_players: int, aq: MessageQueue) -> None:
    set_round_and_color = SetRoundAndWildColor(game_round=1, wild_color=Purple())
    aq.append(set_round_and_color)

    for player in range(number_of_players):
        aq.append(UpdatePlayerScore(player, INITIAL_PLAYER_SCORE))

    aq.append(FillSupplySpaces())  # Handled by GM

    set_phase = SetGamePhase(Phase.acquire_tile)
    aq.append(set_phase)


def phase_one(action: Action, state: State | None, aq: MessageQueue, eq: MessageQueue):
    match action:
        case NewGame(number_of_players=number_of_players):
            handle_new_game(number_of_players, aq)
        case _:
            logger.debug(
                f"function {inspect.currentframe().f_code.co_name} received action {action} and did not reach a matching case"
            )
