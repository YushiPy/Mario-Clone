
from types import ModuleType
from importlib.util import spec_from_file_location, module_from_spec
from os.path import join

import sys

from block import Block
from map import Map
from player import Player

from Settings.sprite import LEVELS_FOLDER_NAME


FOLDER_PATH = join(__file__.rsplit('/', 1)[0], LEVELS_FOLDER_NAME)


def import_module(name: str, path: str) -> ModuleType:
    
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec) # type: ignore
    
    sys.modules[name] = module
    spec.loader.exec_module(module) # type: ignore
    
    return module


def get_level(world: int, level: int) -> tuple[Map, Player]:
    
    module = import_module(f'{world}-{level}.py', join(FOLDER_PATH, f'{world}-{level}.py'))
    
    blocks_info: list[Block] = module.blocks
    initial_pos = module.INITIAL_POS
    
    
    level_map = Map(blocks_info)
    
    return level_map, Player(level_map, initial_pos)
