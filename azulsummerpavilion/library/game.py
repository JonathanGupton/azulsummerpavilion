from dataclasses import dataclass
from typing import Optional

from azulsummerpavilion.library.actions import DistributeTiles
from azulsummerpavilion.library.actions import MakePlayerTileSelection
from azulsummerpavilion.library.actions import MakeTileSelection
from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.components.constants import Bag
from azulsummerpavilion.library.components.state import AzulSummerPavilionState as State
from azulsummerpavilion.library.logic.logic import game_logic
from azulsummerpavilion.library.player_interface import PlayerInterface
from azulsummerpavilion.library.queue import MessageDequeue
from azulsummerpavilion.library.queue import MessageQueue
from azulsummerpavilion.library.random_interface import RandomInterface
from library.components.constants import PLAYER_TO_DISPLAY_RATIO


@dataclass
class AzulSummerPavilionGame:
    players: tuple[PlayerInterface, ...]
    random: RandomInterface
    events: MessageQueue
    actions: MessageQueue
    state: Optional[State] = None

    @classmethod
    def new_game(
        cls,
        players: tuple[PlayerInterface, ...],
        random: RandomInterface,
        actions: Optional[MessageQueue] = None,
        events: Optional[MessageQueue] = None,
    ) -> "AzulSummerPavilionGame":
        """Factory method to create a new game instance.
        Args:
            players: Tuple of PlayerInterface instances (2-4 players required)
            random: RandomInterface instance for game randomization
            actions: Optional MessageQueue
            events: Optional MessageQueue

        Returns:
            New AzulSummerPavilionGame instance

        Raises:
            ValueError: If number of players is not 2, 3, or 4
        """
        if len(players) not in PLAYER_TO_DISPLAY_RATIO:
            raise ValueError(
                f"Invalid number of players: {len(players)}. "
                f"Azul Summer Pavilion requires 2-4 players."
            )

        if actions is None:
            actions = MessageDequeue()
        if events is None:
            events = MessageDequeue()

        # Queue the NewGame action to trigger state initialization
        actions.append(NewGame(len(players)))
        return cls(players=players, random=random, events=events, actions=actions)


class GameManager:
    @staticmethod
    def process_game(game: AzulSummerPavilionGame) -> AzulSummerPavilionGame:
        """
        This function is responsible for handling player actions, random actions (bag draws), and
        calling the game logic to modify the game's state.
        """
        while game.actions:
            aq = game.actions
            action = aq.popleft()
            match action:
                case MakeTileSelection(
                    source=source, tile_count=tile_count, target=target
                ) if isinstance(source, Bag):
                    tiles = game.random.draw(game.state.tiles, draw_count=tile_count)
                    aq.appendleft(
                        DistributeTiles(tiles=tiles, source=source, target=target)
                    )
                case MakePlayerTileSelection():
                    curr = game.state.current_player
                    tile_selection = game.players[curr].get_action(game.state)
                    aq.append(tile_selection)
                case _:
                    aq.appendleft(action)
                    game.state, game.actions, game.events = game_logic(
                        game.actions, game.state, game.events
                    )

        return game
