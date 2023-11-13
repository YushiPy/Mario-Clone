
from pygame import Surface, Vector2

from block import Block
from sprites import load


class BrickBlock(Block):
    
    sprite = load('Overworld Brick Block Top')
    
    def draw(self, surface: Surface, reference: Vector2) -> None:
        return super().draw(surface, reference)