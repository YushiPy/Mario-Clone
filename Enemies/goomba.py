
from enemy import Enemy
from sprites import load

class Goomba(Enemy):

    base_speed = -0.01
    
    dimensions = 1, 1
    hitbox_value = .2, -.3, .6, .4

    death_dimensions = 1, .5

    sprite = load('Goomba Walk 2.png', dimensions, sprite_type='Enemies')
    death_sprite = load('Goomba Stomped', (1, .5), sprite_type='Enemies')
