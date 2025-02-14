from dataclasses import dataclass
from typing import Optional

from azulsummerpavilion.library.actions import DistributeTiles
from azulsummerpavilion.library.actions import MakePlayerTileSelection
from azulsummerpavilion.library.actions import MakeTileSelection
from azulsummerpavilion.library.components.constants import Bag
from azulsummerpavilion.library.components.state import AzulSummerPavilionState as State
from azulsummerpavilion.library.logic.logic import game_logic
from azulsummerpavilion.library.player_interface import PlayerInterface
from azulsummerpavilion.library.queue import MessageQueue
from azulsummerpavilion.library.random_interface import RandomInterface


@dataclass
class AzulSummerPavilionGame:
    players: tuple[PlayerInterface]
    random: RandomInterface
    events: MessageQueue
    actions: MessageQueue
    state: Optional[State] = None


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
