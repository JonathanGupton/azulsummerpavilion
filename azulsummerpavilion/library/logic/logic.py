from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.actions import AdvancePhase
from azulsummerpavilion.library.actions import DiscardFactoryDisplayToCenter
from azulsummerpavilion.library.actions import DistributeTiles
from azulsummerpavilion.library.actions import DoPlayerTurn
from azulsummerpavilion.library.actions import FillFactoryDisplaySpaces
from azulsummerpavilion.library.actions import FillSupplySpaces
from azulsummerpavilion.library.actions import MakePlayerTileSelection
from azulsummerpavilion.library.actions import MoveTilesToPlayerHand
from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.actions import PlayerTileIsSelected
from azulsummerpavilion.library.actions import SetGamePhase
from azulsummerpavilion.library.actions import SetRoundAndWildColor
from azulsummerpavilion.library.actions import SetStartPlayer
from azulsummerpavilion.library.actions import UpdatePlayerScore
from azulsummerpavilion.library.components.constants import FactoryDisplay
from azulsummerpavilion.library.components.constants import Phase
from azulsummerpavilion.library.components.constants import PlayerReserve
from azulsummerpavilion.library.components.constants import Supply
from azulsummerpavilion.library.components.state import AzulSummerPavilionState as State
from azulsummerpavilion.library.components.tiles import factory_displays_are_empty
from azulsummerpavilion.library.components.tiles import table_center_is_empty
from azulsummerpavilion.library.events import PlayerScoreUpdated
from azulsummerpavilion.library.logic.logic_handlers import (
    handle_discard_factory_display_to_center,
)
from azulsummerpavilion.library.logic.logic_handlers import (
    handle_fill_factory_display_spaces_and_enqueue_player_turn,
)
from azulsummerpavilion.library.logic.logic_handlers import handle_fill_supply_spaces
from azulsummerpavilion.library.logic.logic_handlers import handle_move_tiles_to_player_hand
from azulsummerpavilion.library.logic.logic_handlers import handle_new_game
from azulsummerpavilion.library.logic.logic_handlers import handle_player_tile_selection
from azulsummerpavilion.library.logic.logic_handlers import handle_set_game_phase
from azulsummerpavilion.library.logic.logic_handlers import handle_set_round_and_wild_color
from azulsummerpavilion.library.logic.logic_handlers import handle_set_start_player
from azulsummerpavilion.library.queue import MessageQueue


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
            handle_new_game(number_of_players, aq)

        case FillSupplySpaces():
            handle_fill_supply_spaces(aq)

        case FillFactoryDisplaySpaces():
            player_count = state.player_count
            handle_fill_factory_display_spaces_and_enqueue_player_turn(player_count, aq)

        case PlayerTileIsSelected(
            color=color, source=source
        ) if state.phase == Phase.acquire_tile and isinstance(source, FactoryDisplay):
            handle_player_tile_selection(state, color, source, aq)

        case MoveTilesToPlayerHand(
            player=player, selected_color=color, source=source, tiles=tiles
        ):
            handle_move_tiles_to_player_hand(
                state, player, color, source, tiles, aq, eq
            )

            # If source was factory display, queue up the discard action
            if isinstance(source, FactoryDisplay):
                aq.append(
                    DiscardFactoryDisplayToCenter(
                        factory_display_index=source.display_index
                    )
                )

        case SetStartPlayer(player=player):
            handle_set_start_player(state, player, aq, eq)

        case DiscardFactoryDisplayToCenter(factory_display_index=display_index):
            handle_discard_factory_display_to_center(state, display_index, aq, eq)

        case DistributeTiles(tiles=tiles, source=source, target=target) if isinstance(
            target, Supply
        ):

            # TODO:  do the distribution
            aq.append(FillFactoryDisplaySpaces())

        case DistributeTiles(tiles=tiles, source=source, target=target) if isinstance(
            target, FactoryDisplay
        ):
            # TODO:  Implement distribution to Factory Display
            display_index = target.display_index

        case DistributeTiles(tiles=tiles, source=source, target=target) if isinstance(
            target, PlayerReserve
        ) and state.phase == Phase.acquire_tile:

            # TODO:  Move tiles to player reserve, dump remaining tiles to table center
            pass

        case DistributeTiles(tiles=tiles, source=source, target=target) if isinstance(
            target, PlayerReserve
        ) and isinstance(source, Supply):
            # TODO: Implement draw to player reserve from supply
            pass

        case UpdatePlayerScore(player=player, score=score):
            state.score.update(player, score)
            eq.append(
                PlayerScoreUpdated(
                    player=player,
                    change=score,
                    new_score=state.score.player_score(player),
                )
            )

        case SetGamePhase(phase=phase):
            handle_set_game_phase(state, phase, eq)

        case SetRoundAndWildColor(game_round=game_round, wild_color=wild_color):
            handle_set_round_and_wild_color(state, round, wild_color)

        case DoPlayerTurn() if all(
            (
                state.phase == Phase.acquire_tile,
                table_center_is_empty(state.tiles),
                factory_displays_are_empty(state.tiles),
            )
        ):
            aq.append(AdvancePhase())

        case DoPlayerTurn() if state.phase == Phase.acquire_tile and any(
            (
                not table_center_is_empty(state.tiles),
                not factory_displays_are_empty(state.tiles),
            )
        ):
            aq.append(MakePlayerTileSelection())

        case MakePlayerTileSelection():
            pass

        case AdvancePhase() if state.phase == Phase.acquire_tile:
            # TODO:  Implement advance to play tiles
            pass

        case AdvancePhase() if state.phase == Phase.play_tiles:
            # TODO:  Implement advance to prepare_next_round or EndGame()
            pass

        case AdvancePhase() if state.phase == Phase.prepare_next_round:
            # TODO:  Implement advance to acquire_tile
            pass

        case _:
            pass
    return state, aq, eq
