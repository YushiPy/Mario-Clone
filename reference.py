
import pygame as pg

from player import Player
from map import Map

from Settings.screen import SCREEN_CENTER, SCREEN_CENTER_C

class Reference:

    def __init__(self, player: Player, map_sample: Map) -> None:
        
        self.player = player
        self.map = map_sample
        
        self.x_bounds = self.map.x_bounds[0] + SCREEN_CENTER[0], self.map.x_bounds[1] - SCREEN_CENTER_C[0]
        self.y_bounds = self.map.y_bounds[0] + SCREEN_CENTER_C[1] - 1, self.map.y_bounds[1] - SCREEN_CENTER[1]
    
        if self.x_bounds[0] > self.x_bounds[1]: self.x_bounds = self.x_bounds[0], self.x_bounds[0]
        if self.y_bounds[0] > self.y_bounds[1]: self.y_bounds = self.y_bounds[0], self.y_bounds[0]
        
    
    @property
    def x(self) -> float:
        return min(self.x_bounds[1], max(self.x_bounds[0], self.player.centerx))
    
    
    @property
    def y(self) -> float:
        return min(self.y_bounds[1], max(self.y_bounds[0], self.player.centery))
    
    
    @property
    def xy(self) -> pg.Vector2:
        return pg.Vector2(self.x, self.y)
    
    
    def draw(self, surface: pg.Surface) -> None:
        self.player.draw(surface, self.xy)
    
    
    def __sub__(self, __other: pg.Vector2) -> pg.Vector2:
        return self.xy - __other
    

    def __rsub__(self, __other: pg.Vector2) -> pg.Vector2:
        return __other - self.xy