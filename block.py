
from typing import overload
import pygame as pg

from Settings.screen import convert_pos

class Block(pg.Vector2):

    sprite: pg.Surface

    @overload
    def __init__(self, x: tuple[int, int]) -> None: ...
    @overload
    def __init__(self, x: int, y: int) -> None: ...

    def __init__(self, x: tuple[int, int] | int, y: int = 0) -> None:
        
        if isinstance(x, int): return self.__init__((x, y))

        super().__init__(x)

        self.pos = x
    

    def draw(self, surface: pg.Surface, reference: pg.Vector2) -> None:

        surface.blit(self.sprite, convert_pos(self, reference))


    def __repr__(self) -> str:
        return f'Block: {self.pos}'
