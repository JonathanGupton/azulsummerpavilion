"""Module containing classes for referencing board and draw positions"""

from __future__ import annotations

from dataclasses import dataclass

from azulsummerpavilion.library.constants import StarColor
from azulsummerpavilion.library.constants import TileIndex
from azulsummerpavilion.library.constants import TileTarget
from azulsummerpavilion.library.tile_array import TileArray


@dataclass(frozen=True, order=True)
class BoardPosition:
    star: StarColor
    tile_value: int

    def flatten(self) -> int:
        """Convert the 2D (star, tile_value) to the 1D position on the board"""
        return self.star * 6 + self.tile_value - 1

    def __iter__(self):
        yield self.star
        yield self.tile_value

    def __str__(self):
        return f"(star={self.star.name}, value={self.tile_value})"


@dataclass(frozen=True)
class DrawPosition:
    location: TileIndex
    tiles_position: int = 0
    tiles: TileArray = TileArray([0, 0, 0, 0, 0, 0])

    def __str__(self):
        return f"{self.location.name}-{self.tiles_position} - {str(self.tiles)}"

    def as_tile_position(self) -> TilePosition:
        return TilePosition(
            getattr(TileTarget, self.location.name), self.tiles_position
        )


@dataclass
class TilePosition:
    """Dataclass for specifying the location to play a tile to or from which
    to retrieve a tile

    TilePosition is used as an argument in the logic modules
    """

    location: TileTarget
    nth: int = 0

    def __str__(self):
        if self.location in {
            TileTarget.Bag,
            TileTarget.Tower,
            TileTarget.TableCenter,
            TileTarget.Supply,
        }:
            return str(self.location.value)
        else:
            return f"{str(self.location.value)}-{self.nth}"
