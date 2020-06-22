''' utility functions and helpers
'''

from typing import Tuple
from dataclasses import dataclass
import random

from pygame import Rect


@dataclass
class Point:
    'Generic 2D vector'
    x: int
    y: int


def random_position(rect: Rect) -> Point:
    ''' returns tuple of random position bounded by rect '''
    return (random.randint(rect.left, rect.right),
            random.randint(rect.top, rect.bottom))
