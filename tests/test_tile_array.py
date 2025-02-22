import numpy as np
import pytest

from azulsummerpavilion.library.components.constants import TileColor
from azulsummerpavilion.library.components.tile_array import InvalidTileArrayLengthError
from azulsummerpavilion.library.components.tile_array import TileArray


class TestTileArray:
    def test_create_from_list(self):
        # When
        tile_array = TileArray([1, 0, 0, 0, 0, 0])

        # Then
        assert isinstance(tile_array, TileArray)
        assert len(tile_array) == 6
        assert tile_array[0] == 1
        assert all(x == 0 for x in tile_array[1:])

    def test_create_from_numpy_array(self):
        # Given
        np_array = np.array([1, 0, 0, 0, 0, 0], dtype="B")

        # When
        tile_array = TileArray(np_array)

        # Then
        assert isinstance(tile_array, TileArray)
        assert len(tile_array) == 6
        assert tile_array[0] == 1
        assert all(x == 0 for x in tile_array[1:])

    def test_create_empty(self):
        # When
        tile_array = TileArray.new()

        # Then
        assert isinstance(tile_array, TileArray)
        assert len(tile_array) == 6
        assert all(x == 0 for x in tile_array)

    def test_invalid_length_raises_error(self):
        # Then
        with pytest.raises(InvalidTileArrayLengthError):
            TileArray([1, 0, 0, 0, 0])  # Too short

        with pytest.raises(InvalidTileArrayLengthError):
            TileArray([1, 0, 0, 0, 0, 0, 0])  # Too long

    def test_numpy_operations_maintain_type(self):
        # Given
        arr1 = TileArray([1, 0, 0, 0, 0, 0])
        arr2 = TileArray([0, 1, 0, 0, 0, 0])

        # When
        result = arr1 + arr2

        # Then
        assert isinstance(result, TileArray)
        assert np.array_equal(result, [1, 1, 0, 0, 0, 0])

    def test_from_dict(self):
        # Given
        tile_dict = {TileColor.Orange: 1, TileColor.Red: 2}

        # When
        tile_array = TileArray.from_dict(tile_dict)

        # Then
        assert isinstance(tile_array, TileArray)
        assert tile_array[TileColor.Orange] == 1
        assert tile_array[TileColor.Red] == 2
        assert all(tile_array[i] == 0 for i in range(2, 6))

    def test_to_dict(self):
        # Given
        tile_array = TileArray([1, 2, 0, 0, 0, 0])

        # When
        result = tile_array.to_dict()

        # Then
        assert result == {TileColor.Orange: 1, TileColor.Red: 2}

    def test_equality_comparison(self):
        # Given
        arr1 = TileArray([1, 0, 0, 0, 0, 0])
        arr2 = TileArray([1, 0, 0, 0, 0, 0])
        arr3 = TileArray([0, 1, 0, 0, 0, 0])

        # Then
        assert arr1 == arr2
        assert arr1 != arr3
        assert not (arr1 == [1, 0, 0, 0, 0, 0])  # Compare with list

    def test_sum_operation(self):
        # Given
        tile_array = TileArray([1, 2, 3, 0, 0, 0])

        # Then
        assert sum(tile_array) == 6

    def test_maintains_type_after_operations(self):
        # Given
        arr = TileArray([1, 2, 0, 0, 0, 0])

        # Then
        assert isinstance(arr * 2, TileArray)
        assert isinstance(arr + 1, TileArray)
        assert isinstance(arr[0:3], TileArray)
