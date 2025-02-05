from dataclasses import dataclass

from azulsummerpavilion.library.color import Color
from azulsummerpavilion.library.constants import Bag
from azulsummerpavilion.library.constants import Phase
from azulsummerpavilion.library.constants import StarColor
from azulsummerpavilion.library.constants import TileTarget
from azulsummerpavilion.library.tile_array import TileArray


class Message:
    """Base class used for passing and processing events and actions."""

    pass


class Action(Message):
    """Class for action commands that are to be processed by the Game class and the game logic."""

    pass


@dataclass
class NewGame(Action):
    """Command to create a new game"""

    number_of_players: int


@dataclass
class SetRoundAndWildColor(Action):
    """Command to set the round number and the wild color"""

    game_round: int
    wild_color: Color


@dataclass
class MakeTileSelection(Action):
    tile_count: int
    source: TileTarget
    target: TileTarget


@dataclass
class MakePlayerTileSelection(Action):
    pass


@dataclass
class PlayerTileIsSelected(Action):
    """
    Command when a player has selected a tile to draw and information
    needs to be passed to the game logic for processing
    """

    color: Color
    source: TileTarget


@dataclass()
class DistributeTiles(Action):
    """Command to distribute tiles"""

    tiles: TileArray
    source: TileTarget
    target: TileTarget


@dataclass
class SelectTilesToDrawFromBag(Action):
    """Command to select tiles to be drawn from the bag (this command does not draw the tiles)"""

    draw_count: int
    target: TileTarget
    source: TileTarget = Bag()


@dataclass
class SetGamePhase(Action):
    """Set the game phase."""

    phase: Phase


@dataclass
class SetStartPlayer(Action):
    """Set the start player token to the player"""

    player: int


@dataclass
class RemoveStartPlayerToken(Action):
    """Remove the start player token from the player"""

    player: int


@dataclass
class PlayTileToStarAndScore(Action):
    """Play a tile to the board and score"""

    player: int
    player_selected_tiles: TileArray
    target_star: StarColor


@dataclass
class EndGame(Action):
    """Command to end and finalize the game"""


@dataclass
class UpdatePlayerScore(Action):
    """Update the player score"""

    player: int
    score: int


@dataclass
class DoPlayerTurn(Action):
    """Trigger a player turn"""

    pass


@dataclass
class FillSupplySpaces(Action):
    """Begin the process to fill the supply spaces with tiles"""

    pass


@dataclass
class FillFactoryDisplaySpaces(Action):
    """Fill all factory display spaces"""

    pass


@dataclass
class AdvancePhase(Action):
    """Advance the game state to the next phase"""

    pass


@dataclass
class MoveTilesToPlayerHand(Action):
    """Command to move tiles from a source to player's hand following wild tile rules"""

    player: int
    selected_color: Color
    source: TileTarget
    tiles: TileArray


@dataclass
class DiscardFactoryDisplayToCenter(Action):
    """Command to discard remaining tiles from a factory display to the table center"""

    factory_display_index: int
