"""Module containing the Board class"""

from __future__ import annotations

from collections import deque

import numpy as np

from azulsummerpavilion.library.constants import StarColor


class InvalidTilePlacement(Exception):
    pass


class Board:
    """
    Class representing an Azul Summer Pavilion game board
    """

    n_tile_spaces = 6

    def __init__(self, board: np.ndarray) -> None:
        self.board = board

    @classmethod
    def new(cls):
        board = np.zeros(shape=(len(StarColor), cls.n_tile_spaces), dtype="B")
        return cls(board)

    def is_placement_location_open(self, star: StarColor, tile_value: int) -> bool:
        """Validate that the star location is open"""
        return (
            (tile_value >= 1)
            and (tile_value <= 6)
            and (self.board[star, tile_value - 1] == 0)
        )

    def place_tile(self, star: StarColor, tile_value: int) -> int:
        """Place a tile on the board.  Returns the value of the placement."""
        if self.is_placement_location_open(star, tile_value):
            score = self.score_tile_placement(star, tile_value)
            self.board[star, tile_value - 1] = 1
        else:
            raise InvalidTilePlacement(f"Cannot place a tile on {star} {tile_value}")
        return score

    # TODO:  Move score_tile_placement out of the class
    def score_tile_placement(self, star: StarColor, tile_value: int) -> int:
        """
        Compute the score associated with placing a tile on the provided star
        and value location.

        Scoring for placement is 1 plus the count of tiles immediately
        adjacent in the star.

        For example:

         [0, 0, 0, 0, 0, 0]
        - Place at any position 0 to 5 -> 1 point

        [1, 0, 0, 0, 0, 0]
        - Place at 1 or 5 -> 2 points
        - else 1 point

        [1, 0, 1, 0, 0, 0]
        - place at 1 -> 3 points
        - place at 3 -> 2 points
        - place at 4 -> 1 point
        - place at 5 -> 2 points

        [1, 0, 0, 1, 0, 0]
        - place at 1 -> 2 points
        - place at 2 -> 2 points
        - place at 4 -> 2 points
        - place at 5 -> 2 points

        [1, 0, 0, 0, 1, 0]
        - place at 1 -> 2 points
        - place at 2 -> 1 point
        - place at 3 -> 2 points
        - place at 5 -> 3 points
        """
        score = 1
        index = tile_value - 1
        seen = {index}
        q = deque([index])
        while q:
            current = q.popleft()
            left = current - 1 if (current - 1) >= 0 else len(self.board[star]) - 1
            right = current + 1 if (current + 1) <= (len(self.board[star]) - 1) else 0
            if left not in seen and self.board[star, left] == 1:
                q.append(left)
                seen.add(left)
                score += 1
            if right not in seen and self.board[star, right] == 1:
                q.append(right)
                seen.add(right)
                score += 1
        return score
