class PhaseTwoPlayers:
    """Object showing the playing/passing status for each player in Phase Two"""

    def __init__(self, number_of_players: int):
        self.number_of_players = number_of_players
        self.players = [False for _ in range(self.number_of_players)]

    def __repr__(self):
        return f"{__class__.__name__}(self.players={self.players})"

    def __str__(self):
        return self.__repr__()

    def is_playing(self, player) -> bool:
        """Returns if the player is still playing Phase Two."""
        return self.players[player]

    def set_player_to_passing(self, player: int) -> None:
        """Set a player as passing for the remainder of Phase Two."""
        self.players[player] = False

    def initialize_phase_two(self) -> None:
        """Set all players as playing Phase Two at the beginning of the phase."""
        self.players = [True for _ in self.players]

    def all_passing(self) -> bool:
        """Return if all players are passing"""
        return all([status is False for status in self.players])
