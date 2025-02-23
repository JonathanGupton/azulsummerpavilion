"""Module containing the bag draw interface for the GameManager"""

from abc import ABC
from abc import abstractmethod
from collections import deque
from typing import Sequence

import numpy as np

from azulsummerpavilion.library.components.tile_array import TileArray


def validate_draw(tiles: np.ndarray, draw_count: int) -> bool:
    """Draws cannot be less than 0 or greater than the total available tiles"""
    return 0 <= draw_count <= sum(tiles)


class RandomInterface(ABC):
    """
    Base class for the random interface.  This API is used to generate bag draws by the
    GameManager.
    """

    @abstractmethod
    def draw(self, tiles: np.ndarray, draw_count: int) -> TileArray:
        """Given the current tile array, generate an n tile tile-array of tiles to draw"""
        pass


class DeterministicInterface(RandomInterface):
    """
    The deterministic interface returns a provided TileArray rather than a random draw.
    This is used in testing when specific draws are needed and in modeling best-moves.
    """

    def __init__(self, draws: Sequence[TileArray]):
        self.draws = deque(draws)

    def draw(self, tiles: np.ndarray, draw_count: int) -> TileArray:
        return self.draws.popleft()

    def enqueue_draw(self, draws: Sequence[TileArray]):
        self.draws.extend(draws)


class SeededRandomInterface(RandomInterface):
    """
    The SeededInterface accepts a seed value for the RNG in order to have reproducible
    bag draws.
    """

    def __init__(self, seed: int) -> None:
        self.seed = seed
        self.rng: np.random.Generator = np.random.default_rng(seed=seed)

    def draw(self, tiles: np.ndarray, draw_count: int) -> TileArray:
        return TileArray(
            self.rng.multivariate_hypergeometric(tiles, draw_count).astype("B")
        )


class DefaultRandomInterface(RandomInterface):
    """
    The DefaultRandomInterface is the default value used by the GameManager for
    drawing tiles from the bag.  This does not accept a seed for the RNG and will return
    whatever is randomly provided without user input.
    """

    def __init__(self):
        self.rng: np.random.Generator = np.random.default_rng()
        self.seed: int = self.rng.bit_generator.seed_seq.state["entropy"]

    def draw(self, tiles: np.ndarray, draw_count: int) -> TileArray:
        drawn_tiles = self.rng.multivariate_hypergeometric(tiles, draw_count).astype(
            "B"
        )
        drawn_tile_array = TileArray(drawn_tiles.view(TileArray))
        return drawn_tile_array

    def get_seed(self):
        return self.seed
