
from typing import Self, override

from pygame import Surface

from entity import Box, Entity
from map import Map

from Settings.entity import ENEMY_DEATH_TIME, Hitbox

class Enemy(Entity):
    
    base_speed: float
    
    death_sprite: Surface
    death_dimensions: Box | None = None
    
    def __init__(self, map_sample: Map, pos: tuple[int | float, int | float]) -> None:
        super().__init__(map_sample, pos)
        
        self.speed.x = self.base_speed
        self.alive = True
        
        self.death_time = ENEMY_DEATH_TIME # If <= 0: remove from map
    
    
    @override
    def fail_move_x(self) -> None:
        self.speed.x *= -1
    
    
    @override
    def update(self) -> Self:

        self.death_time -= not self.alive

        return super().update()
    
    
    def die(self) -> None:
        
        self.alive = False
        self.sprite = self.death_sprite
        self.speed.x = 0
        
        if self.death_dimensions is None: return
        
        self.y -= self.dimensions[1] - self.death_dimensions[1]
        self.dimensions = self.death_dimensions
        
    
    @override
    def collide(self, __other: Entity | Hitbox) -> bool:
        return self.alive and super().collide(__other)
    