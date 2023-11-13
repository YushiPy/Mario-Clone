
"""
Methods named 'update' should be called every fixed update
"""

import pygame as pg

from pygame import Surface

from PythonModules.game_template import EventHolder, Game, EVENTS_IN_FIXED
from PythonModules.text import Text

Game.start_display()

from enemy_holder import EnemyHolder
from levels import get_level
from reference import Reference

from Settings.sprite import BG_COLOR
from Enemies.goomba import Goomba


class Gameplay(Game):
    def __init__(self, __fps: int | float = 125, __flags: int = 0) -> None:
        super().__init__(__fps, EVENTS_IN_FIXED)
        
        self.map, self.player = get_level(1, 1)
        self.enemy_holder = EnemyHolder(self.player, [Goomba(self.map, (i, int(str(i ** .5)[-1]))) for i in range(8, 100)])
        
        self.reference = Reference(self.player, self.map)
        
        
    def draw(self, surface: Surface) -> Surface | None:
        
        surface.fill(BG_COLOR)
        
        #Text(self.player.xy, (SCREEN_CENTER_P[0], SCREEN_CENTER_P[1] - 100)).draw(surface)
        #Text(self.player.speed, (SCREEN_CENTER_P[0], SCREEN_CENTER_P[1] - 150)).draw(surface)
        #Text(self.reference.xy, (SCREEN_CENTER_P[0], SCREEN_CENTER_P[1] - 200)).draw(surface)
        
        self.map.draw(surface, self.reference.xy)
        self.reference.draw(self.surface)
        self.enemy_holder.draw(surface, self.reference.xy)
        
        return surface
    
    
    def fixed_update(self, down_keys: EventHolder, up_keys: EventHolder, held_keys: EventHolder, events: EventHolder) -> bool | None:
        
        self.player.move(held_keys[pg.K_d] - held_keys[pg.K_a], down_keys[pg.K_SPACE])
        self.enemy_holder.update()
        
        
    def update(self, down_keys: EventHolder, up_keys: EventHolder, held_keys: EventHolder, events: EventHolder) -> bool | None:

        if pg.K_r in down_keys: self.__init__()

print(Gameplay().run().get_info())