
from typing import Iterable

from pygame import Surface, Vector2

from enemy import Enemy
from player import Player

class EnemyHolder(list[Enemy]):
    
    def __init__(self, player: Player, enemies: Iterable[Enemy]) -> None:
        super().__init__(enemies)
        
        self.player = player

        self.deads: list[Enemy] = []
    
    
    def draw(self, surface: Surface, reference: Vector2) -> None:
        
        for i in self:
            i.draw(surface, reference.xy)
    
        
    def update(self) -> None:
        
        for i in self: 
            if not i.update().death_time: self.remove(i)
        
        x = next((i for i in self if i.collide(self.player)), None) 
        
        if x is None: return
        
        if not self.player.hit_type(x): return self.player.get_hit() 
    
        x.die()
    
        self.player.hit_enemy()

