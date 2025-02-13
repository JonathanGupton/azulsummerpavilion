from __future__ import annotations

from abc import ABC


class Color(ABC):
    tile_color: int = None
    star_color: int = None
    wild_phase: int = None

    def __eq__(self, other: Color) -> bool:
        return self.__class__.__name__ == other.__class__.__name__

    def is_wild(self, phase: int) -> bool:
        return self.wild_phase == phase


class Purple(Color):
    tile_color = 5
    star_color = 5
    wild_phase = 0


class Green(Color):
    tile_color = 4
    star_color = 4
    wild_phase = 1


class Orange(Color):
    tile_color = 0
    star_color = 0
    wild_phase = 2


class Yellow(Color):
    tile_color = 3
    star_color = 3
    wild_phase = 3


class Blue(Color):
    tile_color = 2
    star_color = 2
    wild_phase = 4


class Red(Color):
    tile_color = 1
    star_color = 1
    wild_phase = 5


TILE_COLOR_ORDER = [Orange(), Red(), Blue(), Yellow(), Green(), Purple()]
