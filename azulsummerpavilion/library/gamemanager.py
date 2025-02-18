from library.actions import DistributeTiles
from library.actions import MakePlayerTileSelection
from library.actions import MakeTileSelection
from library.components.constants import Bag
from library.game import AzulSummerPavilionGame
from library.logic.logic import game_logic


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
