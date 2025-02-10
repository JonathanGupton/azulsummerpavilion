"""Tests for the Score class"""

import pytest

from azulsummerpavilion.library.score import Score


class TestScore:
    """Test suite for Score class"""

    @pytest.fixture
    def two_player_score(self) -> Score:
        """Fixture providing a two-player score instance"""
        return Score(player_count=2)

    @pytest.fixture
    def four_player_score(self) -> Score:
        """Fixture providing a four-player score instance"""
        return Score(player_count=4)

    class TestInitialization:
        """Tests for Score initialization"""

        def test_creates_with_correct_player_count(self, two_player_score):
            """Test that Score creates with correct number of players"""
            assert len(two_player_score) == 2

        def test_initializes_with_zero_scores(self, two_player_score):
            """Test that all players start with zero points"""
            assert all(score == 0 for score in two_player_score)

    class TestScoreUpdates:
        """Tests for updating player scores"""

        def test_update_increases_player_score(self, two_player_score):
            """Test that update correctly increases a player's score"""
            two_player_score.update(player=0, n_points=5)
            assert two_player_score[0] == 5
            assert two_player_score[1] == 0  # Other player unchanged

        def test_multiple_updates_accumulate(self, two_player_score):
            """Test that multiple updates accumulate correctly"""
            two_player_score.update(player=0, n_points=5)
            two_player_score.update(player=0, n_points=3)
            assert two_player_score[0] == 8

        def test_update_different_players(self, two_player_score):
            """Test that updates to different players work correctly"""
            two_player_score.update(player=0, n_points=5)
            two_player_score.update(player=1, n_points=3)
            assert two_player_score[0] == 5
            assert two_player_score[1] == 3

        def test_update_with_negative_points(self, two_player_score):
            """Test that negative point updates work correctly"""
            two_player_score.update(player=0, n_points=5)
            two_player_score.update(player=0, n_points=-3)
            assert two_player_score[0] == 2

        def test_update_with_negative_to_below_zero_is_zero(self, two_player_score):
            """Test that negative point updates that go below zero work correctly"""
            two_player_score.update(player=0, n_points=3)
            two_player_score.update(player=0, n_points=-5)
            assert two_player_score[0] == 0

        def test_update_with_negative_from_zero_to_below_zero_is_zero(
            self, two_player_score
        ):
            """Test that negative point updates that go from zero to below zero work correctly"""
            two_player_score.update(player=0, n_points=-5)
            assert two_player_score[0] == 0

    class TestPlayerScore:
        """Tests for retrieving player scores"""

        def test_player_score_returns_correct_value(self, two_player_score):
            """Test that player_score returns the correct score"""
            two_player_score.update(player=0, n_points=5)
            assert two_player_score.player_score(0) == 5

        def test_player_score_returns_zero_for_unchanged_player(self, two_player_score):
            """Test that player_score returns 0 for player with no updates"""
            assert two_player_score.player_score(1) == 0

    class TestErrorCases:
        """Tests for error handling"""

        def test_update_invalid_player_raises_error(self, two_player_score):
            """Test that updating invalid player raises IndexError"""
            with pytest.raises(IndexError):
                two_player_score.update(player=2, n_points=5)

        def test_player_score_invalid_player_raises_error(self, two_player_score):
            """Test that accessing invalid player raises IndexError"""
            with pytest.raises(IndexError):
                two_player_score.player_score(2)

    class TestRepresentation:
        """Tests for string representation"""

        def test_repr_format(self, two_player_score):
            """Test the format of __repr__"""
            two_player_score.update(player=0, n_points=5)
            expected = "Score(P0: 5, P1: 0)"
            assert repr(two_player_score) == expected


def test_different_player_counts():
    """Test that Score works with different player counts"""
    scores = {2: Score(2), 3: Score(3), 4: Score(4)}
    assert all(len(score) == count for count, score in scores.items())
