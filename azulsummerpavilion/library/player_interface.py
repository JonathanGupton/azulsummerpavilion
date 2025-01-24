"""Module containing the player interface used to send and receive messages, actions and events
between the players and game manager."""

from abc import ABC
from abc import abstractmethod

from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.player import Player


class PlayerInterface(ABC):
    """API for sending and receiving messages from players"""

    def __init__(self, player: Player) -> None:
        self.player = player

    @abstractmethod
    def get_action(self, action: Action) -> Action:
        """Send an action (request) to the player.  The player responds with their next action."""
        pass
