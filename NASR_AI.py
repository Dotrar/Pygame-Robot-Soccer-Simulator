#nasr example code to work with simulator
#this code is meant to be largely portable

import numpy as np
from math import *
import re

from navsim.helpers import *

#use generator next time
from enum import Enum


class State(Enum):
    SEARCH = 1  # looking for ball
    SURVEY = 11  # rotate on the spot
    ACQUIRE = 2  # drive towards ball
    DRIBBLE = 3  # move with ball
    KICK = 4  # kick into goal
    STOP = 5

    #NASR - Not a Soccer Robot. AI design by D.West n9142461 - dre.west@connect{...}

    #   The AI functions on a basic VFF and kalman filter SLAM method.
    # Using a list of objects to represent the obstructions: with each view, clarifies
    # and more confident in that object's position.
    #   Then, using VFF method, find the best route to travel (towards ball, away from
    # obst.)
    #   Also contains a state machine for multi-goal orientation. Here, the goals are
    # to both get the ball, as well as go towards a soccer-goal.

    # Status: vector FF


def kernel(num):
    k = np.sin(np.linspace(0, pi/2, num))
    kr = np.flip(k, 0)[1:]
    return np.concatenate([k, kr])


class NASR(object):
    def __init__(self, dict_vals):
        #State management
        self.state = State.SEARCH
        self.ball_known = False
        self.ball_possession = False
        self.surveyed_area = False
        self.survey_val = None
        self.enabled = False
        self.oldr = 0
        self.target = 'ball'

        self.ball_nearness = 50
        self.goal_nearness = 300

        #robot control
        self.robot = None

        self.vector_number = 360
        self.vectors = np.zeros(self.vector_number)
        self.smooth = kernel(90)

        self.weights = {
            'obst': -1.2,
            'ball': 0.2,
            'goal': .6
        }

        self.range = dict_vals['sensor_range']

        #mapping
        self.map = []
        self.ball = []
        self.goal = []

        #movement and tracking
        self.pos = (0, 0, 0)
        self.dir = (0, 0, 1)

    def attach_robot(self, robot):
        self.robot = robot

    def prepare(self, pos):
        self.pos = pos

    def convolve(self, kernel):
        v = self.vectors
        tmp = np.concatenate([v, v, v])
        tmp = np.convolve(tmp, kernel, 'same')
        self.vectors = np.array_split(tmp, 3)[1]

    def receive_readout(self, readout):
        #readout should be in the form of:
        #|goal,r,b|obst,r,b|...
        rx, ry, rr = self.pos

        #self.map.clear()

        #print(readout)
        for view in readout.split("|"):
            reading = view.split(',')
            idx = reading[0]
            rb = floatify(reading[1:])
            #global co-ords, robot relative + newdir
            xy = intify(
                (rx + rb[0] * cos(radians(rr+rb[1])),
                 ry + rb[0] * sin(radians(rr+rb[1])))
            )
            #ball
            if idx == 'ball':
                self.ball_known = True
                self.ball = xy
            #goal
            elif idx == 'goal':
                self.goal = xy
            #obstruction
            elif idx == 'obst':
                #see if there's one closest, and update it, otherwise append
                idx = find_similar(xy, self.map)
                if idx is None:
                    self.map.append(xy)
                else:
                    self.map[idx] = xy  # TODO Kalman filter.

    def route(self):
        #make a fake goal and go to it.
        dir = np.argmax(self.vectors)
        range = 0.5
        dr = w180(dir - self.robot.r)
        dr = 0 if dr == 0 else .5 if dr > 0 else -.5
        dxy = pol2rect((range, dir))
        return (dxy[0], dxy[1], dr)

    def survey(self):
        self.dir = (0, 0, 0.5)
        r = self.pos[2]

        if self.survey_val is not None:
            diff_r = w180(r - self.oldr)
            print("survey: old {} new {} diff {} val {}".format(
                self.oldr, r, diff_r, self.survey_val))
            self.oldr = r
            self.survey_val += diff_r
        else:
            self.robot.log('BEGIN SURVEY')
            self.survey_val = 0
            self.oldr = r

        return (self.survey_val > 360)

    def process(self):
        rx, ry, rr = self.pos
        self.vectors.fill(0)
        #map is in global xy
        for ob in self.map:
            x, y = ob
            x -= rx
            y -= ry
            r, b = intify(rect2pol((x, y)))
            if(r > self.range):
                continue
            b = w360(b)
            self.vectors[b] = int(abs(self.range - r)**2/r
                                  * self.weights['obst'])

        #ball
        if self.ball and self.target == 'ball':
            x, y = self.ball
        elif self.goal and self.target == 'goal':
            x, y = self.goal
        else:
            self.convolve(self.smooth)
            return

        x -= rx
        y -= ry
        r, b = intify(rect2pol((x, y)))
        b = w360(b)
        r = int(abs(2000 - r))**2/r

        self.vectors[b] = r * self.weights[self.target]
        self.convolve(self.smooth)

    def action(self):  # set self.dir during this
        if not self.enabled:
            return (0, 0, 0)
        self.dir = (0, 0, 0)
        s = self.state

        # ## SEARCH
        if s == State.SEARCH:
            self.robot.log('SEARCH')
            if self.ball:  # ball is known
                self.robot.log('found ball, acquring')
                self.state = State.ACQUIRE
            elif not self.surveyed_area:  # else we haven't surveyed
                self.robot.log('New area, no ball')
                self.state = State.SURVEY
            else:
                self.robot.log('looking somewhere else')
                return self.route()  # route to unknown place

        # ## SURVEY
        elif s == State.SURVEY:

            has_finished = self.survey()
            if has_finished:
                self.surveyed_area = True
                self.robot.log('finished survey, ball ' +
                               ('found' if self.ball else 'not found'))
                self.state = State.SEARCH

        # ## ACQUIRE
        elif s == State.ACQUIRE:
            self.dir = self.route()
            bx, by = self.ball
            rx, ry, rr = self.pos
            if rect2pol((bx-rx, by-ry))[0] < self.ball_nearness:
                self.ball_possession = True
                self.robot.log('Activate Dribbler')
                self.state = State.DRIBBLE

        elif s == State.DRIBBLE:
            #our target is now the goal
            #TODO search for goal if not known
            self.target = 'goal'
            self.dir = self.route()
            bx, by = self.goal
            rx, ry, rr = self.pos

            r, b = rect2pol((bx-rx, by-ry))
            if r < self.goal_nearness:

                self.robot.log('Kick!')
                xx, yy = pol2rect((r/100, self.robot.r))
                self.robot.w.ball.dx = xx
                self.robot.w.ball.dy = yy
                self.ball_possession = False
                self.state = State.STOP

        elif s == State.KICK:
            pass
        elif s == State.STOP:
            self.robot.log('job done, powering down')
            self.enabled = False
            pass

        return self.dir
