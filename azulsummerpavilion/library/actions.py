from dataclasses import dataclass
from typing import Optional

from azulsummerpavilion.library.constants import Bag
from azulsummerpavilion.library.constants import Phase
from azulsummerpavilion.library.constants import TileColor
from azulsummerpavilion.library.constants import StarColor
from azulsummerpavilion.library.constants import TileTarget
from azulsummerpavilion.library.state import AzulSummerPavilionState as State
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

    round: int


@dataclass()
class DistributeTiles(Action):
    """Command to distribute tiles from the bag"""

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
class DistributeTilesToSupply(Action):
    """Command to move tiles from the bag to the supply spaces"""

    tiles: TileArray


@dataclass
class DistributeTilesToFactoryDisplays(Action):

    tile_count: int
    factory_display: int


@dataclass
class SetGamePhase(Action):
    """Set the game phase."""

    phase: Phase


@dataclass
class PickTilesFromFactoryDisplay(Action):
    """Pick the tile(s) from the Factory Display"""

    factory_display: int
    tile: TileColor
    player: int


@dataclass
class PickTilesFromTableCenter(Action):
    """Pick the tile(s) from the Table Center"""

    tile: TileColor
    player: int


@dataclass
class AssignStartPlayerToken(Action):
    """Assign the start player token to the player"""

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
class PassAndEndPlayForPhase(Action):
    """Command for ending a player's turns in a phase"""

    player: int
    saved_tiles: TileArray


@dataclass
class EndGame(Action):
    """Command to end and finalize the game"""


@dataclass
class UpdatePlayerScore(Action):
    """Update the player score"""

    player: int
    score: int


@dataclass
class CompleteInitialization(Action):
    """Complete the initialization process and trigger the game start"""

    pass


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
    pass


@dataclass
class MakeTileSelection(Action):
    tile_count: int
    source: TileTarget
    target: TileTarget
