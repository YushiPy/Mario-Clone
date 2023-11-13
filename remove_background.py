
from typing import Iterable
from PIL import Image

import os

type Color = tuple[int, int, int, int]

def remove(path: str, colors: Iterable[Color]) -> None:
    
    colors_to_remove = set(colors)

    image = Image.open(path).convert('RGBA')
    
    new_data = [i if i not in colors_to_remove else (0, 0, 0, 0) for i in image.getdata()]
    
    image.putdata(new_data) # type: ignore
    image.save(path, 'PNG')


def clear_folder(path: str, colors: Iterable[Color]) -> None:
    
    colors = set(colors)
    
    paths = [i for i in os.listdir(path) if i != '.DS_Dtore']
    paths = [os.path.join(FOLDER_PATH, i) for i in paths]

    for i in paths: 
        remove(i, colors)

color = (128, 118, 255, 255)
color = (127, 119, 255, 255)
# color = (58, 127, 255, 255)

FOLDER_PATH = os.path.join('Sprites', 'Enemies')

clear_folder(FOLDER_PATH, [color])