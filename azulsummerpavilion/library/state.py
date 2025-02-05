from dataclasses import dataclass
from typing import Optional

from azulsummerpavilion.library.board import Board
from azulsummerpavilion.library.color import Color
from azulsummerpavilion.library.constants import Phase
from azulsummerpavilion.library.score import Score
from azulsummerpavilion.library.tiles import Tiles


@dataclass
class AzulSummerPavilionState:
    player_count: int
    tiles: Tiles
    score: Score
    boards: list[Board]
    current_player: Optional[int] = 0
    phase: Optional[Phase] = None
    round: Optional[int] = None
    wild_color: Optional[Color] = None
    initializing: Optional[bool] = None
    start_player: Optional[int] = None

    @classmethod
    def new(cls, player_count: int) -> "AzulSummerPavilionState":
        """Instantiate the necessary game components and returns a new initial game state"""
        tiles = Tiles.new(player_count)
        score = Score(player_count)
        boards = [Board.new() for _ in range(player_count)]
        return cls(
            player_count=player_count,
            tiles=tiles,
            score=score,
            boards=boards,
            initializing=True,
        )
