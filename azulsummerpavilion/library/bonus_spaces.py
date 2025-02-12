from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator
from typing import Sequence

from azulsummerpavilion.library.board import Board
from azulsummerpavilion.library.constants import StarColor
from azulsummerpavilion.library.position import BoardPosition

_PILLAR_POSITIONS: Sequence[Sequence[BoardPosition]] = (
    (
        BoardPosition(StarColor.Orange, 2),
        BoardPosition(StarColor.Orange, 3),
        BoardPosition(StarColor.Wild, 6),
        BoardPosition(StarColor.Wild, 1),
    ),
    (
        BoardPosition(StarColor.Red, 2),
        BoardPosition(StarColor.Red, 3),
        BoardPosition(StarColor.Wild, 1),
        BoardPosition(StarColor.Wild, 2),
    ),
    (
        BoardPosition(StarColor.Blue, 2),
        BoardPosition(StarColor.Blue, 3),
        BoardPosition(StarColor.Wild, 2),
        BoardPosition(StarColor.Wild, 3),
    ),
    (
        BoardPosition(StarColor.Yellow, 2),
        BoardPosition(StarColor.Yellow, 3),
        BoardPosition(StarColor.Wild, 3),
        BoardPosition(StarColor.Wild, 4),
    ),
    (
        BoardPosition(StarColor.Green, 2),
        BoardPosition(StarColor.Green, 3),
        BoardPosition(StarColor.Wild, 4),
        BoardPosition(StarColor.Wild, 5),
    ),
    (
        BoardPosition(StarColor.Purple, 2),
        BoardPosition(StarColor.Purple, 3),
        BoardPosition(StarColor.Wild, 5),
        BoardPosition(StarColor.Wild, 6),
    ),
)

_STATUE_POSITIONS: Sequence[Sequence[BoardPosition]] = (
    (
        BoardPosition(StarColor.Orange, 1),
        BoardPosition(StarColor.Orange, 2),
        BoardPosition(StarColor.Red, 3),
        BoardPosition(StarColor.Red, 4),
    ),
    (
        BoardPosition(StarColor.Red, 1),
        BoardPosition(StarColor.Red, 2),
        BoardPosition(StarColor.Blue, 3),
        BoardPosition(StarColor.Blue, 4),
    ),
    (
        BoardPosition(StarColor.Blue, 1),
        BoardPosition(StarColor.Blue, 2),
        BoardPosition(StarColor.Yellow, 3),
        BoardPosition(StarColor.Yellow, 4),
    ),
    (
        BoardPosition(StarColor.Yellow, 1),
        BoardPosition(StarColor.Yellow, 2),
        BoardPosition(StarColor.Green, 3),
        BoardPosition(StarColor.Green, 4),
    ),
    (
        BoardPosition(StarColor.Green, 1),
        BoardPosition(StarColor.Green, 2),
        BoardPosition(StarColor.Purple, 3),
        BoardPosition(StarColor.Purple, 4),
    ),
    (
        BoardPosition(StarColor.Purple, 1),
        BoardPosition(StarColor.Purple, 2),
        BoardPosition(StarColor.Orange, 3),
        BoardPosition(StarColor.Orange, 4),
    ),
)

_WINDOW_POSITIONS: Sequence[Sequence[BoardPosition]] = (
    (
        BoardPosition(StarColor.Orange, 5),
        BoardPosition(StarColor.Orange, 6),
    ),
    (
        BoardPosition(StarColor.Red, 5),
        BoardPosition(StarColor.Red, 6),
    ),
    (
        BoardPosition(StarColor.Blue, 5),
        BoardPosition(StarColor.Blue, 6),
    ),
    (
        BoardPosition(StarColor.Yellow, 5),
        BoardPosition(StarColor.Yellow, 6),
    ),
    (
        BoardPosition(StarColor.Green, 5),
        BoardPosition(StarColor.Green, 6),
    ),
    (
        BoardPosition(StarColor.Purple, 5),
        BoardPosition(StarColor.Purple, 6),
    ),
)


@dataclass(frozen=True)
class Pillar:
    adjacent: tuple[int, ...]
    draw_count: int = 1


@dataclass(frozen=True)
class Statue:
    adjacent: tuple[int, ...]
    draw_count: int = 2


@dataclass(frozen=True)
class Window:
    adjacent: tuple[int, ...]
    draw_count: int = 3


class BonusSpace:
    """
    Base class to unite windows, pillars and statues bonus spaces under a
    single API
    """

    _positions = [_PILLAR_POSITIONS, _STATUE_POSITIONS, _WINDOW_POSITIONS]
    _bonus_space_classes = [Pillar, Statue, Window]

    def __init__(self):
        self._bonus_space: set[Pillar | Statue | Window] = set()
        for _class_positions, _class in zip(self._positions, self._bonus_space_classes):
            for group in _class_positions:
                positions: tuple[int, ...] = tuple(p.flatten() for p in group)
                self._bonus_space.add(_class(positions))

    def surrounded_spaces(self, board: Board) -> Iterator[Pillar | Statue | Window]:
        for space in self._bonus_space:
            if all(board.board.flatten().take(space.adjacent)):
                yield space

    def remove_space(self, space: Pillar | Statue | Window):
        self._bonus_space.remove(space)
