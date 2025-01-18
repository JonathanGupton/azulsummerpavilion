"""Module containing the player interface used to send and receive messages, actions and events
between the players and game manager."""

from abc import ABC
from abc import abstractmethod

from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.events import Event
from azulsummerpavilion.library.player import Player


class PlayerInterface(ABC):
    """API for sending and receiving messages from players"""

    def __init__(self, player: Player) -> None:
        self.player = player

    @abstractmethod
    def send_event(self, event: Event):
        """Send an event to the player."""
        pass

    @abstractmethod
    def send_action(self, action: Action) -> Action:
        """Send an action (request) to the player.  The player responds with their next action."""
        pass
