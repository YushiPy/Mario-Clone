
from math import ceil

from PythonModules.game_template import WIDTH, HEIGHT

from Settings.screen import SCREEN_SIZE

BLOCK_SIZE = ceil(WIDTH / SCREEN_SIZE[0]), ceil(HEIGHT / SCREEN_SIZE[1])
