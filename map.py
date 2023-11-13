
from math import ceil, floor
from typing import Iterable, overload
import pygame as pg

from block import Block

from Settings.screen import SCREEN_CENTER, SCREEN_CENTER_C

class Map(dict[tuple[int, int], Block]):
    
    def __init__(self, blocks: Iterable[Block]) -> None:
        super().__init__([(i.pos, i) for i in blocks])
        
        self.x_bounds = min(int(i.x) for i in blocks), max(int(i.x) for i in blocks)
        self.y_bounds = min(int(i.y) for i in blocks), max(int(i.y) for i in blocks) + 1
        
        self.bounds = self.x_bounds, self.y_bounds
        
        
    def drawable(self, reference: pg.Vector2) -> list[Block]:
        
        xbounds = floor(reference.x - SCREEN_CENTER[0]), ceil(reference.x + SCREEN_CENTER_C[0]) + 1
        ybounds = floor(reference.y - SCREEN_CENTER_C[1]), ceil(reference.y + SCREEN_CENTER[1]) + 1
        
        values = []
        
        for y in range(*ybounds):
            for x in range(*xbounds):
                if (x, y) in self:
                    values.append(self[(x, y)])
    
        return values
    
    
    def draw(self, surface: pg.Surface, reference: pg.Vector2) -> None:
        
        for i in self.drawable(reference):
            i.draw(surface, reference)
            
    @overload
    def valid_pos(self, x: tuple[int, int]) -> bool: ...
    @overload
    def valid_pos(self, x: int, y: int) -> bool: ...
    
    def valid_pos(self, x: tuple[int, int] | int, y: int = 0) -> bool:
        
        if isinstance(x, tuple): return self.valid_pos(*x)
        
        return (x, y) not in self and self.x_bounds[0] <= x < self.x_bounds[1] and y >= self.y_bounds[0]