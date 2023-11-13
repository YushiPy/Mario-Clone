
from textwrap import wrap
from itertools import chain
from typing import Callable, TypeVar, Dict, Any

from pygame import Rect
import pygame

pygame.init()
pygame.font.init()

fonts: dict[tuple[str, int, bool, bool], pygame.font.Font] = {}

default_font = 'ヒラキノ角コシックw0', 30, False, False

vertical_spacing = 1.5

writable_keys: set[int | str] = {32, 39, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 
                     57, 59, 61, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 
                     107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 
                     " ", "'", ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                     ';', '=', '[', '\\', ']', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

shift_map = {' ' : ' ', '`' : '~', '1' : '!', '2' : '@', '3' : '#', '4' : '$', '5' : '%', 
             '6' : '^', '7' : '&', '8' : '*', '9' : '(', '0' : ')', '-' : '_', '=' : '+', 
             '[' : '{', ']' : '}', '\\' : '|', ';' : ':', ',' : '<', '.' : '>', '/' : '?', 
             "'" : '"','a' : 'A', 'b' : 'B', 'c' : 'C', 'd' : 'D', 'e' : 'E', 'f' : 'F', 
             'g' : 'G', 'h' : 'H', 'i' : 'I', 'j' : 'J', 'k' : 'K', 'l' : 'L', 'm' : 'M', 
             'n' : 'N', 'o' : 'O', 'p' : 'P', 'q' : 'Q', 'r' : 'R', 's' : 'S', 't' : 'T', 
             'u' : 'U', 'v' : 'V', 'w' : 'W', 'x' : 'X', 'y' : 'Y', 'z' : 'Z'}

_T = TypeVar('_T')

def text_cache(function: Callable[..., _T]) -> Callable[..., _T]:
    
    def wrapper(instance: 'Text', *args, **kwargs) -> _T:
        
        if instance.cache.get(function) is None:
            instance.cache[function] = function(instance, *args, **kwargs)

        return instance.cache[function]
    
    return wrapper


class Text:

    def __init__(self, 
                 value: _T, first_center: tuple[int, int] = (0, 0), 
                 font_info: tuple[str, int, bool, bool] = default_font, 
                 text_color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] | None = None,
                 represent: Callable[[_T], str] = str, alignment: Callable[[Rect], Rect] = lambda rect: rect,
                 antialias: bool = True,
                 multiline_style: int = 1, max_horizontal: int | None = None, vertical_spacing: int = vertical_spacing,
                 alpha: int = 255, alpha_range: tuple[int, int] = (0, 255)) -> None:

        self.__initialized = False
        
        self.cache: Dict[Callable[..., _T], (_T | None)] = {}

        self.value = value
        self.first_center = first_center
        self.text_color = text_color
        self.background_color = background_color
        self.represent = represent
        self.alignment = alignment
        self.antialias = antialias

        self.font_info = font_info
        self.font = get_font(*font_info)

        self.max_horizontal = max_horizontal
        self.vertical_spacing = vertical_spacing
        self.multiline_style = multiline_style
 
        self.alpha = alpha
        self.alpha_range = alpha_range

        self.association: Text | None = None

        self.__initialized = True


    @property
    @text_cache
    def surfaces(self) -> list[pygame.Surface]:
        
        def text_surfaces(self: Text, lines: list[str]) -> list[pygame.Surface]:
            
            text_surfaces = [self.font.render(i, self.antialias, self.text_color, self.background_color) 
                             for i in lines]
            
            for i in text_surfaces: 
                i.set_alpha(round(self.alpha))

            return text_surfaces

        if not self.max_horizontal:
            return text_surfaces(self, self.represent(self.value).split('\n'))

        max_chars = self.max_horizontal // (3 * self.font_info[1] // 8)
        string = self.represent(self.value)

        lines = chain.from_iterable(wrap(i, max_chars) for i in string.split('\n')) if string else ['']

        return text_surfaces(self, lines)


    @property
    @text_cache
    def rects(self) -> list[pygame.Rect]:
        
        rects = [i.get_rect() for i in self.surfaces]

        rects[0].centery = self.first_center[1]
        for i in range(1, len(rects)):
            rects[i].y = rects[i - 1].y + self.vertical_spacing * rects[i - 1].height

        rects[0].centerx = self.first_center[0]

        dy = (rects[0].y + rects[-1].bottom) // 2 - self.first_center[1]

        for i in rects: 
            align(rects[0], i, self.multiline_style)
            i.y -= dy

        return [self.alignment(i) for i in rects]


    @property
    @text_cache
    def rect(self) -> pygame.Rect:

        rects = self.rects

        x = min(rect.x for rect in rects)
        y = rects[0].y
        width = max(rect.width for rect in rects)
        height = rects[-1].bottom - y

        return pygame.Rect(x, y, width, height)


    def draw(self, surface: pygame.Surface, texts: list['Text'] = [], spacing: list[int | float] | None = None, fade_rate: int | float = 0) -> pygame.Surface:

        self.alpha = max(self.alpha_range[0], min(self.alpha_range[1], self.alpha - fade_rate))

        for a, b in zip(self.surfaces, self.rects):
            surface.blit(a, b)

        if not texts: return surface
        if spacing is None: spacing = []

        spacing = spacing + [vertical_spacing] * (len(texts) - len(spacing) + 1)

        base_y = self.rects[-1].y + spacing[0] * self.rects[-1].height

        for text, space in zip(texts, spacing[1:]): 
            for a, b in zip(text.surfaces, text.rects):
                rect = align(self.rect, b.copy(), self.multiline_style)
                rect.y -= text.rects[0].y - base_y

                surface.blit(a, rect)

            base_y = rect.y + space * rect.height
            
        return surface


    def associate_rects(self, other: 'Text', spacing: int | float = vertical_spacing, permanent: bool = False):

        if permanent: 
            self.__dict__['spacing'] = spacing
            self.__dict__['association'] = other

        rect = align(other.rects[-1], self.rect.copy(), other.multiline_style)
        rect.y = other.rects[-1].y + spacing * other.rects[-1].height

        self.__dict__['first_center'] = rect.center

        return self


    def __setattr__(self, __name: str, __value: Any) -> None:
        
        self.__dict__[__name] = __value

        if not self.__initialized: return

        for i in self.cache: self.cache[i] = None

        if not self.association is None: self.associate_rects(self.association, self.spacing)
    

def get_font(__name: str, __size: int, __bold: bool = False, __italic: bool = False) -> pygame.font.Font:

    if (__name, __size, __bold, __italic) in fonts:
        return fonts[(__name, __size, __bold, __italic)]
        
    fonts[(__name, __size, __bold, __italic)] = pygame.font.SysFont(__name, __size, __bold, __italic)

    return fonts[(__name, __size, __bold, __italic)]


def align(base_rect: pygame.Rect, aligned_rect: pygame.Rect, style: int = 0) -> pygame.Rect:
    
    base_rect = pygame.Rect(*base_rect)

    if style == 0: aligned_rect.x = base_rect.x
    if style == 1: aligned_rect.centerx = base_rect.centerx
    if style == 2: aligned_rect.left = base_rect.left

    return aligned_rect
