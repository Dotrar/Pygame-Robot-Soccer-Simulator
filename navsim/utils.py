''' utility functions and helpers
'''

from typing import Tuple
from dataclasses import dataclass
import random

from pygame import Rect # type: ignore


@dataclass
class Point:
    'Generic 2D vector'
    x: int
    y: int

@dataclass
class Obstacle:
    pos: Point
    size: int

def random_position(rect: Rect) -> Point:
    ''' returns tuple of random position bounded by rect '''
    return Point(random.randint(rect.left, rect.right),
            random.randint(rect.top, rect.bottom))
