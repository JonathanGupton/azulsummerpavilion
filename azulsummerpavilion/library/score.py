import numpy as np


class Score(np.ndarray):
    """Base class for player scores

    Score is a subclassed np.ndarray with a length of the number of players
    (n_players).  Score is initialized to the start value of 5 points per
    player.
    """

    def __new__(cls, player_count, *args, **kwargs):
        obj = np.asarray([0] * player_count, dtype=np.uint16).view(cls)
        return obj

    def __array_finalize__(self, obj):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'P{i}: {n}' for i, n in enumerate(self)])})"

    def update(self, player: int, n_points: int):
        """Increase/decrease the player's score by n_points"""
        self[player] += n_points

    def player_score(self, player: int) -> int:
        return self[player]
