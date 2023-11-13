
from abc import ABC

from typing import Any

import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 1512, 945
CENTER = CENTERX, CENTERY = WIDTH // 2, HEIGHT // 2

FPS = 125
TIME_STEP = 1000 / 125
if int(TIME_STEP) == TIME_STEP: TIME_STEP = int(TIME_STEP)

clock = pygame.time.Clock()

# Flags

EVENTS_IN_FIXED = 1
SAVE_SURFACE = 2
USE_GLOBAL_DISPLAY = 4
START_DISPLAY = 8

_flags_count = 4

class Game(ABC):
    
    __global_display: pygame.Surface | None = None
    
    def __init__(self, __fps: int | float = 125, __flags: int = 0) -> None:

        flags = [i == '1' for i in f'{__flags:b}'.zfill(_flags_count)[::-1]]

        self.__EVENTS_IN_FIXED = flags[0]
        self.__SAVE_SURFACE = flags[1]
        self.__USE_GLOBAL_DISPLAY = flags[2]
        self.__START_DISPLAY = flags[3]
        
        if self.__START_DISPLAY: Game.start_display()

        self.down_keys: EventHolder = EventHolder()
        self.up_keys: EventHolder = EventHolder()
        self.events: EventHolder = EventHolder()
        self.held_keys: EventHolder = EventHolder()

        self.__all_events: list[EventHolder[int]] = [self.down_keys, self.up_keys, self.held_keys, self.events]

        self.__base_surface: pygame.Surface | None = None
        self.surface = self.__display if self.__USE_GLOBAL_DISPLAY else pygame.Surface((WIDTH, HEIGHT))

        __time_step = 1000 / __fps
        self.TIME_STEP = int(__time_step) if int(__time_step) == __time_step else __time_step

        self.__accumulator = 0

        self.fps_tracker = 0
        self.game_loop_tracker = 0

        self.__run_game = True

        self.__times = []


    @property
    def __display(self) -> pygame.Surface:
        
        if Game.__global_display is not None: return Game.__global_display
        
        Game.__global_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        
        return Game.__global_display
    
    
    @property
    def base_surface(self) -> pygame.Surface:
        
        if self.__base_surface is not None: return self.__base_surface
        
        self.__base_surface = self.set_base_surface(pygame.Surface((WIDTH, HEIGHT)))

        return self.__base_surface
    

    def set_base_surface(self, surface: pygame.Surface) -> pygame.Surface | None:
        pass


    def draw(self, surface: pygame.Surface) -> pygame.Surface | None:
        pass


    def fixed_update(self, down_keys: 'EventHolder', up_keys: 'EventHolder', held_keys: 'EventHolder', 
                     events: 'EventHolder') -> None | bool:
        pass


    def update(self, down_keys: 'EventHolder', up_keys: 'EventHolder', held_keys: 'EventHolder', 
               events: 'EventHolder') -> None | bool:
        pass


    def __rendering_update(self) -> None:

        if not self.__SAVE_SURFACE:
            base = pygame.Surface((WIDTH, HEIGHT)) if self.base_surface is None else self.base_surface.copy()            
            (self.__display if self.__USE_GLOBAL_DISPLAY else self.surface).blit(base, (0, 0))
            

            if self.__USE_GLOBAL_DISPLAY:
                self.surface.blit(base, (0, 0))
            
        self.draw(self.__display if self.__USE_GLOBAL_DISPLAY else self.surface)

        if not self.__USE_GLOBAL_DISPLAY: self.__display.blit(self.surface, (0, 0))
        
        pygame.display.flip()

    
    def start(self) -> None: 
        pass


    def end(self) -> None: 
        pass


    def run(self):

        self.start()
           
        if self.__SAVE_SURFACE and self.base_surface:
            self.surface.blit(self.base_surface, (0, 0))
        
        
        self.start_time = __start = pygame.time.get_ticks()

        while self.__run_game:
            self.ellapsed_time = pygame.time.get_ticks() - self.start_time
            
            self.__times.append(__start)
            __start = self.__loop(__start)
            
            
        self.end_time = __start

        self.end()

        return self
    

    def __loop(self, __start: int) -> int:
        
        if not self.__EVENTS_IN_FIXED: self.__manage_events()

        while self.__accumulator >= self.TIME_STEP:
        
            self.game_loop_tracker += 1
            self.__accumulator -= self.TIME_STEP
        
            if self.__EVENTS_IN_FIXED: self.__manage_events()
            
            if self.fixed_update(*self.__all_events) is not None: self.__run_game = False


        if self.update(*self.__all_events) is not None: self.__run_game = False

        self.fps_tracker += 1
        self.__rendering_update()

        __end = pygame.time.get_ticks()

        self.delta_time = __end - __start
        self.__accumulator += self.delta_time

        return __end


    def __manage_events(self) -> tuple['EventHolder', 'EventHolder', 'EventHolder', 'EventHolder']:

        game_events = pygame.event.get()

        self.down_keys.clear()
        self.up_keys.clear()
        self.events.clear()

        for i in game_events:
            if i.type == pygame.KEYDOWN: self.down_keys.add(i.key)
            elif i.type == pygame.KEYUP: self.up_keys.add(i.key)
            else: self.events.add(i.type)

        if pygame.QUIT in self.events: self.__run_game = False
        if pygame.K_ESCAPE in self.down_keys: self.__run_game = False

        self.held_keys.update(self.down_keys)
        self.held_keys.difference_update(self.up_keys)

        return self.down_keys, self.up_keys, self.held_keys, self.events


    def get_info(self, stringify: bool = True, precision: int = 3) -> str | tuple[float, float]:

        if not self.fps_tracker or not self.game_loop_tracker:
            if not stringify: return 0, 0

            return f"The game apparently hasn't been ran yet, " + \
                    "rendering it impossible to determine any information about its behavior"

        fps = 1000 * self.fps_tracker / (self.end_time - self.start_time)
        game_fps = 1000 * self.game_loop_tracker / (self.end_time - self.start_time)

        if not stringify: return fps, game_fps

        fps, game_fps = round(fps, precision), round(game_fps, precision)

        expected_fps = round(1000 / self.TIME_STEP, 3)

        message_1 = f'The game ran, on average, at {fps} fps'
        message_2 = f'The game loop was called {game_fps} times per seconds'
        message_3 = f'Expected: {expected_fps}, Difference: {round(game_fps - expected_fps, 3)}'

        return f'{message_1}\n{message_2}\n{message_3}'
    
    
    @staticmethod
    def start_display() -> None:
        Game.__global_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    

class EventHolder(set[int]):
    def __getitem__(self, key: int) -> bool:
        return key in self