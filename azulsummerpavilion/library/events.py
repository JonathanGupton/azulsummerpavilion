from dataclasses import dataclass

from azulsummerpavilion.library.actions import Message
from azulsummerpavilion.library.constants import Phase
from azulsummerpavilion.library.state import AzulSummerPavilionState as State


class Event(Message):
    """Base class for event classes that emit information to the players or for logging."""

    pass


@dataclass
class GameInitialized(Event):
    """Message the creation of a new game"""

    state: State


@dataclass
class RoundSet(Event):
    """Message the setting of a round as well as the wild tile"""

    pass


@dataclass
class TilesSelectedToDrawFromBag(Event):
    """Message the selection of tiles to be drawn from the bag"""

    pass


@dataclass
class TilesDistributedToSupply(Event):
    """Message the tiles distributed to the supply from the bag"""

    pass


@dataclass
class GamePhaseSet(Event):
    """Message the setting of the game phase"""

    phase: Phase


@dataclass
class PlayerScoreUpdated(Event):
    """Message a change in player score"""

    player: int
    change: int
    new_score: int
