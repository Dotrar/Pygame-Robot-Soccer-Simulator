''' components that make up any ai system '''
import numpy as np
from ..utils import convolve
from math import pi


class VectorHistogram:
    ''' Vector Hisogram of various size '''

    def __init__(self, size: int, smooth: int = 90):
        self.vectors = np.zeros(size)
        self.smooth = np.sin(np.linspace(0, pi, smooth))
        self.len = len(self.vectors)


    def clear(self):
        self.vectors.fill(0)

    def convolve(self):
        self.vectors = convolve(self.smooth,self.vectors)

    def add(self, position:int, weight:float):
        self.vectors[position % self.len] = weight