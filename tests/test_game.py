import pytest

from azulsummerpavilion.library.actions import NewGame
from azulsummerpavilion.library.game import AzulSummerPavilionGame
from azulsummerpavilion.library.queue import MessageQueue
from conftest import MockPlayer
from conftest import mock_player
from conftest import mock_random


class TestGame:
    def test_game_initialization(self, mock_player, mock_random):
        # When
        game = AzulSummerPavilionGame.new_game(
            players=(mock_player, mock_player), random=mock_random
        )

        # Then
        assert isinstance(game.actions, MessageQueue)
        assert isinstance(game.events, MessageQueue)
        assert game.state is None
        assert len(game.actions) == 1
        assert isinstance(game.actions.popleft(), NewGame)

    @pytest.mark.parametrize("player_count", [2, 3, 4])
    def test_game_initialization_multiple_players(self, player_count, mock_random):
        # Given
        players = tuple(MockPlayer() for _ in range(player_count))

        # When
        game = AzulSummerPavilionGame.new_game(players=players, random=mock_random)

        # Then
        assert len(game.players) == player_count
        new_game_action = game.actions.popleft()
        assert isinstance(new_game_action, NewGame)
        assert new_game_action.number_of_players == player_count

    @pytest.mark.parametrize("player_count", [0, 5])
    def test_game_initialization_fails_with_invalid_player_counts(
        self, player_count, mock_random
    ):
        players = tuple(MockPlayer() for _ in range(player_count))

        with pytest.raises(ValueError):
            AzulSummerPavilionGame.new_game(players=players, random=mock_random)
