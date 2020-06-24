''' utility functions and helpers
'''

from typing import Tuple
from dataclasses import dataclass
import random
import math
import numpy as np

from pygame import Rect


@dataclass
class Point:
    '''Generic 2D vector'''
    x: int
    y: int


@dataclass
class Bearing:
    '''Polar co-ords'''
    b: int
    r: int


def random_position(rect: Rect) -> Point:
    ''' returns tuple of random position bounded by rect '''
    return (random.randint(rect.left, rect.right),
            random.randint(rect.top, rect.bottom))

def wrap180(angle: int) -> int:
    return (angle+180)%360 -180