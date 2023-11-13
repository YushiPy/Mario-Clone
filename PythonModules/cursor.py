
from typing import Any
from PythonModules.colors import Color
from pygame import Surface

import pygame as pg

pg.init()


class Cursor:

    def __init__(self, size: int, color: Color) -> None:
        
        self.__size = size
        self.__color = color

        self.surfaces = self.__surfaces()


    @property
    def size(self) -> int:
        return self.__size
    

    @size.setter
    def size(self, __value: int) -> None:
        self.__size = __value

        self.__update()


    @property
    def color(self) -> Color:
        return self.__color
    

    @color.setter
    def color(self, __value: Color) -> None:
        self.__color = __value

        self.__update()


    def __update(self) -> None:
        self.surfaces = self.__surfaces()


    def __surfaces(self) -> list[Surface]:

        surfaces = [Surface((2 * self.size, 2 * self.size)) for _ in range(self.size)]
        [pg.draw.circle(a, self.color, (self.size, self.size), i) for i, a in enumerate(surfaces)]
        [(a.set_colorkey((0, 0, 0)), a.set_alpha(255 * (1 - i / self.size))) for i, a in enumerate(surfaces, 1)]

        return surfaces
    

    def draw(self, surface: Surface) -> Surface | None:
        
        pg.mouse.set_visible(False)

        pos = [i - self.size for i in pg.mouse.get_pos()]

        for i in self.surfaces:
            surface.blit(i, pos)

        return surface
    
