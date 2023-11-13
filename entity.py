
from abc import ABC
from math import ceil, floor
from typing import Self
import pygame as pg

from map import Map

from Settings.block import BLOCK_SIZE
from Settings.entity import collide_hitbox, GRAVITY
from Settings.screen import convert_pos

type Coordinate = tuple[int, int]
type Box = tuple[float, float]
type Hitbox = tuple[float, float, float, float]

class Entity(ABC, pg.Vector2):
    """
    The positions registered at self represent the entity's sprite's topleft

    Hitboxes follow the following pattern:
        x, y (both relative to the sprite), width and height
    """
    
    dimensions: Box
    hitbox_value: Hitbox
    
    sprite: pg.Surface
    
    def __init__(self, map_sample: Map, pos: tuple[int | float, int | float]) -> None:
        super().__init__(pos)
        
        self.map = map_sample
        self.speed = pg.Vector2(0, 0)
        self.alive = True
        

    @property
    def width(self) -> float:
        return self.dimensions[0]


    @property
    def height(self) -> float:
        return self.dimensions[1]
    

    @property
    def left(self) -> float:
        return self.x
    
    
    @left.setter
    def left(self, x: float) -> None:
        self.x = x
    
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    
    @right.setter
    def right(self, x: float) -> None:
        self.x = x - self.width
        
    
    @property
    def top(self) -> float:
        return self.y


    @top.setter
    def top(self, y: float) -> None:
        self.y = y
        

    @property
    def bottom(self) -> float:
        return self.y - self.height
    
    
    @bottom.setter
    def bottom(self, y: float) -> None:
        self.y = y + self.height
    
    
    @property
    def centerx(self) -> float:
        return self.left + self.width / 2
    
    
    @centerx.setter
    def centerx(self, x: float) -> None:
        self.x = x - self.width / 2
    
    
    @property
    def centery(self) -> float:
        return self.bottom + self.height / 2
    
    
    @centery.setter
    def centery(self, y: float) -> None:
        self.y = y - self.height / 2
    
    
    @property
    def center(self) -> tuple[float, float]:
        return self.centerx, self.centery
    
    
    @center.setter
    def center(self, xy: tuple[float, float]) -> None:
        self.centerx, self.centery = xy
    
    
    @property
    def hitbox(self) -> Hitbox:
        """Rectangle representing x, y, width and height"""

        x, y = self.left + self.hitbox_value[0], self.top + self.hitbox_value[1]
        width, height = self.hitbox_value[2], self.hitbox_value[3]

        return x, y, width, height


    def collide(self, __other: 'Entity | Hitbox') -> bool:
        
        other = __other.hitbox if isinstance(__other, Entity) else __other
        
        return collide_hitbox(self.hitbox, other)


    def draw(self, surface: pg.Surface, reference: pg.Vector2) -> None:
        
        surface.blit(self.sprite, convert_pos(self, reference))
        
        pg.draw.rect(surface, (0, 255, 0), (convert_pos(pg.Vector2(self.x, self.top), reference), (BLOCK_SIZE[0] * self.width, BLOCK_SIZE[1] * self.height)), 3)
        pg.draw.rect(surface, (255, 0, 0), (convert_pos(pg.Vector2(self.hitbox[:2]), reference), (BLOCK_SIZE[0] * self.hitbox[2], BLOCK_SIZE[1] * self.hitbox[3])), 3)
        
    
    def move(self) -> None:
        
        self.speed.y -= GRAVITY
        
        self.try_move()
    
    
    def successful_move_x(self) -> None: 
        self.x += self.speed.x
    
    
    def fail_move_x(self) -> None: 
        
        if self.speed.x > 0:
            self.right = floor(self.right + self.speed.x)
        else:
            self.left = ceil(self.left + self.speed.x)
            
        self.speed.x = 0
    
    
    def successful_move_y(self) -> None:
        self.y += self.speed.y
    
    
    def fail_move_y(self) -> None:

        if self.speed.y > 0:
            self.top = floor(self.top + self.speed.y)
        else:
            self.bottom = ceil(self.bottom + self.speed.y)
            
        self.speed.y = 0
    
    
    def try_move_x(self) -> None:
        
        if all(map(self.map.valid_pos, self.horizontal_blocks())): self.successful_move_x()
        else: self.fail_move_x()
                
    
    def try_move_y(self) -> None:
        
        if all(map(self.map.valid_pos, self.vertical_blocks())): self.successful_move_y()
        else: self.fail_move_y()
    
    
    def try_move(self) -> None:
        
        self.try_move_x()
        self.try_move_y()


    def horizontal_blocks(self, reduction: float = 1e-6) -> list[Coordinate]:
        
        base_x = floor((self.right if self.speed.x > 0 else self.left) + self.speed.x)
        
        return [(base_x, i) for i in range(ceil(self.bottom + reduction), ceil(self.top) + 1)]


    def vertical_blocks(self) -> list[Coordinate]:
        
        base_y = ceil((self.top if self.speed.y > 0 else self.bottom) + self.speed.y)

        return [(i, base_y) for i in range(floor(self.left), ceil(self.right))]


    def blocks_to_check(self, reduction: float = 1e-6) -> tuple[list[Coordinate], list[Coordinate]]:
        return self.horizontal_blocks(reduction), self.vertical_blocks()


    def update(self) -> Self:
        
        self.move()
        
        return self
