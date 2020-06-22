''' utility functions and helpers
'''

from typing import Tuple
import random

Rect = Tuple[int, int, int, int]
Position = Tuple[int, int]


def random_position(rect: Rect) -> Position:
    ''' returns tuple of random position bounded by rect '''
    return (random.randint(rect[0], rect[0]+rect[2]),
            random.randint(rect[1], rect[1]+rect[3]))
