
"""
Hitboxes follow the following pattern:
    x, y (both relative to the sprite), width and height
"""

type Hitbox = tuple[float, float, float, float]

def collide_hitbox(hitbox1: Hitbox, hitbox2: Hitbox) -> bool:
    
    a, b = hitbox1, hitbox2
    
    return a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and a[1] < b[1] + b[3] and a[1] + a[3] > b[1]

PLAYER_MAX_SPEED = 0.1
PLAYER_ACCELERATION = 0.005
PLAYER_JUMP_FORCE = 0.2

PLAYER_DIMENSIONS = 1, 1
PLAYER_HITBOX = .15, -.3, 0.7, 0.7

FRICTION = 0.002 # Should be smaller than acceleration
GRAVITY = 0.003

ENEMY_DEATH_TIME = 100 # Ticks