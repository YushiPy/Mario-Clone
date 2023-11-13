
from typing import override

from entity import Entity
from sprites import load

from Settings.entity import PLAYER_ACCELERATION, PLAYER_DIMENSIONS, PLAYER_HITBOX, PLAYER_JUMP_FORCE, PLAYER_MAX_SPEED, FRICTION, collide_hitbox

type Point = tuple[int, int]
type Hitbox = tuple[float, float, float, float]

class Player(Entity):

    dimensions = PLAYER_DIMENSIONS
    hitbox_value = PLAYER_HITBOX

    sprite = load('Small Mario Stand.png', dimensions)


    def jump(self, override_condition: bool = False) -> None:
        
        if not override_condition and not any(map(self.map.__contains__, self.vertical_blocks())): return

        self.speed.y += PLAYER_JUMP_FORCE
    
    
    @override
    def move(self, x: int, jump: bool = False) -> None:
        
        self.speed.x = max(0, self.speed.x - FRICTION) if self.speed.x > 0 else min(0, self.speed.x + FRICTION)
        self.speed.x = max(-PLAYER_MAX_SPEED, min(PLAYER_MAX_SPEED, self.speed.x + PLAYER_ACCELERATION * x))
        
        if jump: self.jump()
        
        super().move()


    def get_hit(self) -> None:
        self.sprite = load('Small Mario Jump.png', self.dimensions)
        
    
    def hit_enemy(self) -> None:
        
        self.speed.y = 0
        self.jump(True)
        
        self.try_move_y()
    
    
    def hit_type(self, __other: Entity) -> bool:
        """True -> Player hit Enemy, False -> Enemy hit Player"""
    
        hitbox = self.hitbox
        
        frontal = collide_hitbox((hitbox[0] - self.speed.x,) + hitbox[1:], __other.hitbox)
        vertical = collide_hitbox((hitbox[0], hitbox[1] - self.speed.y,) + hitbox[2:], __other.hitbox)
        
        return frontal and not vertical
    