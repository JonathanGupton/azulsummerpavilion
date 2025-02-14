from dataclasses import dataclass
from typing import Optional

from azulsummerpavilion.library.components.board import Board
from azulsummerpavilion.library.components.color import Color
from azulsummerpavilion.library.components.constants import Phase
from azulsummerpavilion.library.components.phasetwo import PhaseTwoPlayers
from azulsummerpavilion.library.components.score import Score
from azulsummerpavilion.library.components.tiles import Tiles


@dataclass
class AzulSummerPavilionState:
    player_count: int
    tiles: Tiles
    score: Score
    boards: list[Board]
    current_player: Optional[int] = 0
    game_end = False
    final = False
    phase: Optional[Phase] = None
    round: Optional[int] = None
    wild_color: Optional[Color] = None
    initializing: Optional[bool] = None
    start_player: Optional[int] = None
    phase_two_players: Optional[PhaseTwoPlayers] = None

    @classmethod
    def new(cls, player_count: int) -> "AzulSummerPavilionState":
        """Instantiate the necessary game components and returns a new initial game state"""
        tiles = Tiles.new(player_count)
        score = Score(player_count)
        boards = [Board.new() for _ in range(player_count)]
        phase_two_players = PhaseTwoPlayers(player_count)
        return cls(
            player_count=player_count,
            tiles=tiles,
            score=score,
            boards=boards,
            initializing=True,
            phase_two_players=phase_two_players,
        )
