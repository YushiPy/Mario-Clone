
from ast import Tuple
from collections.abc import Iterable, Iterator
from typing import Optional, SupportsInt, Union, Self, Iterable

from random import randint, choices
from itertools import repeat, cycle, islice

from copy import copy

import re

class Color(tuple[int, int, int]):

    def __new__(cls, __rgb: Iterable[SupportsInt] = ...) -> Self:

        values = [int(x) for x in islice(__rgb, 3)]

        return super().__new__(cls, values if len(values) == 3 else values + [0] * (3 - len(values)))


    def lighten(self, rate: float = 0.5) -> 'Color':
        return Color(min(255, max(0, round(x + (255 - x) * rate))) for x in self)


    def darken(self, rate: float = 0.5) -> 'Color':
        return Color(min(255, max(0, round(x * (1 - rate)))) for x in self)
    
    
    def dark_lighten(self, rate: float = 0.5) -> 'Color':
        
        if rate <= 0: return Color((0, 0, 0))
        if rate >= 1: return Color((255, 255, 255))
        
        if rate <= 0.5: return Color(x * 2 * rate for x in self)
        
        return Color(x + (255 - x) * (2 * (rate - 0.5)) for x in self)


    def mix(self, color: 'Color', weight_1: float = 1, weight_2: float = 1) -> 'Color':
        
        new_value = [((a * weight_1 / (weight_1 + weight_2) + b * weight_2 / (weight_1 + weight_2))) // 2
                    for a, b in zip(self, color)]

        return Color(new_value)


    def colors_range(self, end: 'Color', number: int = 256) -> Union[list['Color'], 'Color']:

        if number <= 1: return [Color(self)] * int(number)

        offset = tuple(b - a for a, b in zip(self, end))

        return [Color(round(a + i * b / number) for a, b in zip(self, offset)) for i in range(number)]


    @staticmethod
    def random_colors(number: int = 1, start: Optional['Color'] | None = None, end: Optional['Color'] | None = None, 
                      module: bool = False) -> list['Color']:

        if start is None: start = Color((0, 0, 0))
        if end is None: end = Color((255, 255, 255))

        if module: list_of_colors = choices(colors_list)
        else: list_of_colors = [Color([randint(min(a, b), max(a, b)) for a, b in zip(start, end)]) 
                                for _ in repeat(None, number)]

        return list_of_colors


    def __len__(self) -> int:
        return 3


    def __str__(self) -> str:
        return f'Color: {super().__str__()}'



# Colors (Variables)

green = Color((0, 255, 0))
green_minecraft_cactus = Color((92, 117, 94))

ocean_blue = Color((15, 17, 26))
blue = Color((0, 0, 255))
blue_dark_cyan = Color((0, 100, 100))
blue_light_cyan = Color((0, 255, 255))
blue_turquoise = Color((64, 224, 208))
blue_sky = Color((135, 206, 235))


brown = Color((102, 51, 0))
gold = Color((212, 175, 55))
yellow = Color((255, 255, 0))


orange = Color((255, 127, 0))


black = Color((0, 0, 0))
grey = Color((107, 109, 106))
grey_light = Color((157, 159, 156))
grey_silver = Color((216, 216, 216))
white = Color((255, 255, 255))


purple = Color((70, 0, 169))
purple_magenta = Color((138, 0, 255))


pink = Color((255, 0, 255))
pink_light = Color((255, 192, 203))
pink_shocking = Color((255, 0, 132))
pink_flamingo = Color((252, 108, 133))


red = Color((255, 0, 0))
wine = Color((114, 47, 55))
red_blood = Color((104, 0, 0))
red_light = Color((112, 83, 83))
red_white = Color((141, 117, 117))
red_dark = Color((30, 5, 14))


with open(__file__, 'r') as file:

    colors_list = [Color(int(x) for x in rgb) for rgb in re.findall(r'= (\d+), (\d+), (\d+)', file.read())]
    colors_cycle = cycle(colors_list)
