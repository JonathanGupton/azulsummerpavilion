import pytest

from azulsummerpavilion.library.agents import random_interface
from azulsummerpavilion.library.components import tiles
from azulsummerpavilion.library.components.tile_array import TileArray


@pytest.fixture
def default_random_interface():
    return random_interface.DefaultRandomInterface()


@pytest.fixture
def tiles_two_players():
    t = tiles.Tiles.new(2)
    return t


class TestValidateDraws:
    @pytest.mark.parametrize("draws", [-1, 133])
    def test_less_than_0_and_greater_than_total_is_invalid(
        self, tiles_two_players, draws
    ):
        assert not random_interface.validate_draw(tiles_two_players.view_bag(), draws)

    @pytest.mark.parametrize("draws", [i for i in range(133)])
    def test_draws_gt_0_and_lte_tile_sum_are_valid(self, tiles_two_players, draws):
        assert random_interface.validate_draw(tiles_two_players.view_bag(), draws)


class TestDefaultRandomInterface:
    def test_default_random_interface_can_be_instantiated(self):
        # Should not error
        random_interface.DefaultRandomInterface()

    def test_get_seed_returns_seed_value(self, default_random_interface):
        seed = default_random_interface.get_seed()
        assert seed

    @pytest.mark.parametrize("draws", [i for i in range(133)])
    def test_draw_returns_tile_array(
        self, default_random_interface, tiles_two_players, draws
    ):
        draw = default_random_interface.draw(tiles_two_players.view_bag(), draws)
        assert isinstance(draw, TileArray)

    @pytest.mark.parametrize("draws", [i for i in range(133)])
    def test_draw_draws_correct_number_of_tiles(
        self, default_random_interface, tiles_two_players, draws
    ):
        draw = default_random_interface.draw(tiles_two_players.view_bag(), draws)
        assert sum(draw) == draws
