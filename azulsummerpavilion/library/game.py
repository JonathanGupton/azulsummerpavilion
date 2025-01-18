from typing import Optional
from dataclasses import dataclass
from dataclasses import field

from azulsummerpavilion.library.logic import game_logic
from azulsummerpavilion.library.player_interface import PlayerInterface
from azulsummerpavilion.library.queue import MessageDequeue
from azulsummerpavilion.library.random_interface import RandomInterface
from azulsummerpavilion.library.state import AzulSummerPavilionState as State


@dataclass
class AzulSummerPavilionGame:
    players: tuple[PlayerInterface]
    random: RandomInterface
    state: Optional[State] = None
    events: MessageDequeue = field(default_factory=MessageDequeue)
    actions: MessageDequeue = field(default_factory=MessageDequeue)


class GameManager:
    @staticmethod
    def process_game(game: AzulSummerPavilionGame) -> AzulSummerPavilionGame:
        """
        This function is responsible for handling player actions, random actions (bag draws), and
        calling the game logic to modify the game's state.
        """
        while game.actions:
            action = game.actions.popleft()
            match action:
                case _:
                    game.state, game.actions, game.events = game_logic(
                        game.actions, game.state, game.events
                    )
            return game
