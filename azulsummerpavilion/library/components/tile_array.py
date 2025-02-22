from typing import Sequence

import numpy as np

from azulsummerpavilion.library.components.constants import TileColor


class InvalidTileArrayLengthError(Exception):
    pass


class TileArray(np.ndarray):
    """Class to message the movement of tiles from one tile location to another.

    A TileArray is a 1-dimensional array of length 6, representing the count of each tile color.
    The array uses numpy's 'B' (unsigned char) dtype to ensure positive integers and memory efficiency.
    """

    def __new__(cls, input_array: Sequence[int] | np.ndarray):
        # Convert input to numpy array if it isn't already
        obj = np.asarray(input_array, dtype="B").flatten()

        # Validate length
        if len(obj) != 6:
            raise InvalidTileArrayLengthError(
                f"Invalid tile length of {len(obj)}. Must be len of 6."
            )

        # Create the ndarray instance of our type
        obj = obj.view(cls)

        return obj

    def __array_finalize__(self, obj):
        """Handle array creation through view casting or template creation"""
        if obj is None:
            return

    def __ne__(self, other) -> bool:
        """Implement inequality comparison"""
        if not isinstance(other, (TileArray, np.ndarray)):
            return NotImplemented
        return not np.array_equal(self, other)

    def __eq__(self, other) -> bool:
        """Implement equality comparison"""
        if not isinstance(other, (TileArray, np.ndarray)):
            return NotImplemented
        return np.array_equal(self, other)

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
    def new(cls) -> "TileArray":
        """Create an empty TileArray"""
        return cls(np.zeros(6, dtype="B"))

    def __eq__(self, other) -> bool:
        """Implement equality comparison"""
        if not isinstance(other, (TileArray, np.ndarray)):
            return NotImplemented
        return np.array_equal(self, other)
