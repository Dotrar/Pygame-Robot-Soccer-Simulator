''' NASR - AI module
designed to be portable
'''
import typing
import numpy as np
from math import *
from enum import Enum
from .components.vfh import VectorHistogram

#NASR - Not a Soccer Robot. AI design by D.West n9142461 - dre.west@connect{...}

#   The AI functions on a basic VFF and kalman filter SLAM method.
# Using a list of objects to represent the obstructions: with each view, clarifies
# and more confident in that object's position.
#   Then, using VFF method, find the best route to travel (towards ball, away from
# obst.)
#   Also contains a state machine for multi-goal orientation. Here, the goals are
# to both get the ball, as well as go towards a soccer-goal.

''' Ai Components:
        all ai components need to have the following methods:

        receive(self, input:str ) -> None:
            "receives a readout from sensor module"

        command(self) -> str:
            "string command to send to movement platform"

        process(self)->None:
            "called every tick"

'''


class State(Enum):
    ''' enumerate state machine values '''
    SEARCH = 1  # looking for ball
    SURVEY = 11  # rotate on the spot
    ACQUIRE = 2  # drive towards ball
    DRIBBLE = 3  # move with ball
    KICK = 4  # kick into goal
    STOP = 5


def kernel(num):
    k = np.sin(np.linspace(0, pi/2, num))
    kr = np.flip(k, 0)[1:]
    return np.concatenate([k, kr])


class Nasr:
    ''' Not a Soccer Robot original code'''

    def __init__(self):
        self.state = State.SEARCH
        self.vectors = VectorHistogram(360)

        #weightings of observations
        self.weights = {
            'obst': -1.2,
            'ball': 0.2,
            'goal': .6
        }

    def receive(self, readout: str):

        for reading in readout.split('|'):
            obj, distance, angle = reading.split(',')

    def command(self) -> str:
        pass

    def process(self):
        ''' State machine operation '''

        # state machine
        if self.state == State.SEARCH:
            self.search()
        elif self.state == State.SURVEY:
            self.survey()
        elif self.state == State.ACQUIRE:
            self.acquire()
        elif self.state == State.DRIBBLE:
            self.dribble()
        elif self.state == State.KICK:
            self.kick()
        elif self.state == State.STOP:
            self.stop()

            #=====================================================================
            #=====================================================================

        def survey(self):
            ''' find all that is around'''

        def search(self):
            ''' find ball and goal'''

        def acquire(self):
            ''' move towards ball to pick up'''

        def dribble(self):
            ''' hold ball and move towards goal '''

        def kick(self):
            ''' kick ball into goal '''

        def stop(self):
            ''' stop '''
