
from pygame import Vector2

from PythonModules.game_template import SIZE, WIDTH, HEIGHT

def convert_pos(vector: Vector2, reference: Vector2 | None = None) -> tuple[int, int]:
    
    result = vector if reference is None else vector - reference
    
    x = int((result.x + SCREEN_CENTER[0]) * SIZE[0] / SCREEN_SIZE[0])
    y = int((-result.y + SCREEN_CENTER[1]) * SIZE[1] / SCREEN_SIZE[1])
    
    return x, y

SCREEN_SIZE = 24, 15 # Blocks
SCREEN_CENTER = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 # Blocks
SCREEN_CENTER_C = SCREEN_SIZE[0] - SCREEN_CENTER[0], SCREEN_SIZE[1] - SCREEN_CENTER[1] # Blocks

SCREEN_CENTER_P = WIDTH * SCREEN_CENTER[0] // SCREEN_SIZE[0], HEIGHT * SCREEN_CENTER[1] // SCREEN_SIZE[1] # Pixels
