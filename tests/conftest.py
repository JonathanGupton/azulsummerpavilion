from typing import Sequence

import pytest

from azulsummerpavilion.library.actions import Action
from azulsummerpavilion.library.agents.player_interface import PlayerInterface
from azulsummerpavilion.library.agents.random_interface import RandomInterface
from azulsummerpavilion.library.components.constants import TileColor
from azulsummerpavilion.library.components.state import AzulSummerPavilionState as State
from azulsummerpavilion.library.components.tile_array import TileArray
from azulsummerpavilion.library.game import AzulSummerPavilionGame


class MockPlayer(PlayerInterface):
    def __init__(self, actions=None):
        self.actions = actions or []
        self.states_seen = []

    def get_action(self, state: State) -> Action:
        self.states_seen.append(state)
        return self.actions.pop(0) if self.actions else None


class MockRandom(RandomInterface):
    def __init__(self, draws=None):
        self.draws = draws or []
        self.draw_calls = []

    def draw(self, tiles: TileArray, draw_count: int) -> Sequence[TileColor]:
        self.draw_calls.append((tiles, draw_count))
        return self.draws.pop(0) if self.draws else []


@pytest.fixture
def mock_player():
    return MockPlayer()


@pytest.fixture
def mock_random():
    return MockRandom()


@pytest.fixture
def two_player_game(mock_random):
    players = tuple(MockPlayer() for _ in range(2))
    return AzulSummerPavilionGame.new_game(players=players, random=mock_random)


@pytest.fixture
def three_player_game(mock_random):
    players = tuple(MockPlayer() for _ in range(3))
    return AzulSummerPavilionGame.new_game(players=players, random=mock_random)


@pytest.fixture
def four_player_game(mock_random):
    players = tuple(MockPlayer() for _ in range(4))
    return AzulSummerPavilionGame.new_game(players=players, random=mock_random)


@pytest.fixture
def game_start_state_2_players():
    return State.new(2)


@pytest.fixture
def game_start_state_3_players():
    return State.new(3)


@pytest.fixture
def game_start_state_4_players():
    return State.new(4)
