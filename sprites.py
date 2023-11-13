
from functools import cache
import os
import pygame as pg

from Settings.block import BLOCK_SIZE
from Settings.sprite import SPRITES_FOLDER_NAME, SPRITES_FOLDER_LIST, IMAGE_EXTENSION

FOLDER_PATH = f'{__file__.rsplit('/', 1)[0]}/{SPRITES_FOLDER_NAME}'

def load(name: str, size: tuple[float, float] | None = None, sprite_type: int | str | None = None) -> pg.Surface:
    """size's units should be in game blocks"""
    return __load(name, size, sprite_type)

@cache
def __load(name: str, size: tuple[int, int] | None = None, sprite_type: int | str | None = None) -> pg.Surface:
    
    size = BLOCK_SIZE if size is None else (BLOCK_SIZE[0] * size[0], BLOCK_SIZE[1] * size[1])
    
    path = __get_path(name, sprite_type)
    
    image = pg.image.load(path)
    image = pg.transform.scale(image, size).convert_alpha()
    
    image.set_colorkey((0, 0, 0), pg.RLEACCEL)
    
    return image


@cache
def __get_path(name: str, sprite_type: str | int | None = None) -> str:
    
    if isinstance(sprite_type, str): return __make_path(name, sprite_type)
    if isinstance(sprite_type, int): return __make_path(name, SPRITES_FOLDER_LIST[sprite_type])
    
    name2 = (name + IMAGE_EXTENSION).replace(2 * IMAGE_EXTENSION, IMAGE_EXTENSION)
    
    folder = next(i for i in os.listdir(FOLDER_PATH) if  i != '.DS_Store' and name2 in os.listdir(os.path.join(FOLDER_PATH, i)))

    return __make_path(name, folder)
    

@cache
def __make_path(name: str, specific: str, extension: str = IMAGE_EXTENSION) -> str:
    return os.path.join(FOLDER_PATH, specific, name + extension).replace(2 * IMAGE_EXTENSION, IMAGE_EXTENSION)
