from azulsummerpavilion.library.actions import DoPlayerTurn
from azulsummerpavilion.library.actions import FillSupplySpaces
from azulsummerpavilion.library.actions import MakeTileSelection
from azulsummerpavilion.library.actions import MoveTilesToPlayerHand
from azulsummerpavilion.library.actions import SetGamePhase
from azulsummerpavilion.library.actions import SetRoundAndWildColor
from azulsummerpavilion.library.actions import SetStartPlayer
from azulsummerpavilion.library.actions import UpdatePlayerScore
from azulsummerpavilion.library.components.color import Color
from azulsummerpavilion.library.components.color import Purple
from azulsummerpavilion.library.components.constants import Bag
from azulsummerpavilion.library.components.constants import FACTORY_SPACE_DRAW
from azulsummerpavilion.library.components.constants import FactoryDisplay
from azulsummerpavilion.library.components.constants import INITIAL_PLAYER_SCORE
from azulsummerpavilion.library.components.constants import PLAYER_TO_DISPLAY_RATIO
from azulsummerpavilion.library.components.constants import Phase
from azulsummerpavilion.library.components.constants import SUPPLY_SPACE_COUNT
from azulsummerpavilion.library.components.constants import Supply
from azulsummerpavilion.library.components.constants import TileTarget
from azulsummerpavilion.library.components.state import AzulSummerPavilionState
from azulsummerpavilion.library.components.tile_array import TileArray
from azulsummerpavilion.library.events import GamePhaseSet
from azulsummerpavilion.library.queue import MessageQueue


def handle_new_game(number_of_players: int, aq: MessageQueue) -> None:
    set_phase = SetGamePhase(Phase.acquire_tile)
    aq.append(set_phase)

    set_round_and_color = SetRoundAndWildColor(game_round=1, wild_color=Purple())
    aq.append(set_round_and_color)

    for player in range(number_of_players):
        aq.append(UpdatePlayerScore(player, INITIAL_PLAYER_SCORE))

    aq.append(FillSupplySpaces())  # Handled by GM


def handle_fill_supply_spaces(aq: MessageQueue) -> None:
    make_supply_space_selection = MakeTileSelection(
        target=Supply(),
        source=Bag(),
        tile_count=SUPPLY_SPACE_COUNT,
    )
    aq.appendleft(make_supply_space_selection)


def handle_fill_factory_display_spaces_and_enqueue_player_turn(
    player_count: int, aq: MessageQueue
) -> None:
    number_of_displays = PLAYER_TO_DISPLAY_RATIO[player_count]
    for display_index in reversed(range(number_of_displays)):
        make_factory_display_selection = MakeTileSelection(
            target=FactoryDisplay(display_index),
            source=Bag(),
            tile_count=FACTORY_SPACE_DRAW,
        )
        aq.appendleft(make_factory_display_selection)

    aq.append(DoPlayerTurn())


def handle_set_game_phase(
    state: AzulSummerPavilionState, phase: Phase, eq: MessageQueue
) -> None:
    state.phase = phase
    eq.append(GamePhaseSet(phase))


def handle_set_round_and_wild_color(
    state: AzulSummerPavilionState, game_round, wild_color
) -> None:
    state.round = game_round
    state.wild_color = wild_color


def handle_player_tile_selection(
    state: AzulSummerPavilionState,
    color: Color,
    source: TileTarget,
    aq: MessageQueue,
) -> None:
    """Handle a player's tile selection from a factory display"""
    selected_tiles = TileArray.new()

    # Handle wild color selection
    if color == state.wild_color:
        if (
            state.tiles.view_factory_display_n(source.display_index)[color.tile_color]
            > 0
        ):
            selected_tiles[color.tile_color] = 1
    else:
        # Handle regular color selection
        selected_tiles[color.tile_color] = state.tiles.view_factory_display_n(
            source.display_index
        )[color.tile_color]

        # Check for additional wild tile
        if (
            state.tiles.view_factory_display_n(source.display_index)[
                state.wild_color.tile_color
            ]
            > 0
        ):
            selected_tiles[state.wild_color.tile_color] = 1

    aq.append(
        MoveTilesToPlayerHand(
            player=state.current_player,
            selected_color=color,
            source=source,
            tiles=selected_tiles,
        )
    )


def handle_set_start_player(
    state: AzulSummerPavilionState,
    player: int,
    aq: MessageQueue,
    eq: MessageQueue,
) -> None:
    """Handle setting the current player"""
    state.start_player = player  # Set start_player when it was None

    # Apply the -5 point penalty for being first to take from center
    aq.append(UpdatePlayerScore(player=player, score=-5))


def handle_move_tiles_to_player_hand(
    state: AzulSummerPavilionState,
    player: int,
    color: Color,
    source: TileTarget,
    tiles: TileArray,
    aq: MessageQueue,
    eq: MessageQueue,
) -> None:
    """Handle moving tiles to player's hand following wild tile rules"""
    if isinstance(source, FactoryDisplay):
        # Use the specific method for drawing from factory display
        state.tiles.draw_from_factory_display(
            player=player, factory_display=source.display_index, tiles=tiles
        )
    else:
        # For other sources (like table center), use the general move_tiles method
        source_index = state.tiles.table_center_index
        destination_index = state.tiles.player_reserve_index + player
        state.tiles.move_tiles(
            source_index=source_index, destination_index=destination_index, tiles=tiles
        )

        # If start_player is None and taking from table center,
        # set current player as start_player and apply penalty
        if state.start_player is None:
            aq.append(
                SetStartPlayer(
                    player=player  # Use the current player as the start player
                )
            )

    # Queue next player's turn
    aq.append(DoPlayerTurn())


def handle_discard_factory_display_to_center(
    state: AzulSummerPavilionState,
    factory_display_index: int,
    aq: MessageQueue,
    eq: MessageQueue,
) -> None:
    """Handle discarding remaining tiles from factory display to table center"""
    state.tiles.discard_from_factory_display_to_center(
        factory_display=factory_display_index
    )
