from typing import Sequence

from azulsummerpavilion.library.components.constants import TileColor


class InvalidTileArrayLengthError(Exception):
    pass


class TileArray(tuple):
    """Class to message the movement of tiles from one tile location to another"""

    def __new__(cls, tiles: Sequence[int]):
        if len(tiles) != 6:
            raise InvalidTileArrayLengthError(
                f"Invalid tile length of {len(tiles)}. Must be len of 6."
            )
        tile_array = super().__new__(cls, tiles)
        return tile_array

    def __str__(self):
        tile_dict = self.to_dict()
        return str({k.name: v for k, v in tile_dict.items()})

    @classmethod
    def from_dict(cls, tiles: dict[TileColor, int]) -> "TileArray":
        """Create a TileArray from a dict of TileColor: Counts"""
        return cls([tiles.get(i, 0) for i in TileColor])

    def to_dict(self) -> dict[TileColor, int]:
        """Returns a dict of {TileColor: Counts} for the TileArray"""
        return {TileColor(i): count for i, count in enumerate(self) if count > 0}

    @classmethod
    def new(cls):
        """Create an empty TileArray"""
        return cls((0, 0, 0, 0, 0, 0))
