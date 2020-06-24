import math
import numpy as np

from .objects import World
from .utils import Point, Bearing, wrap180
from .robots import Robot
from . import ConfigurationManager
from dataclasses import dataclass

@dataclass
class Obstacle:
    pos: Point 
    radius: int

class Camera(object):
    ''' Camera Sensor class, used for input to the robot; getting world data
    and turning to string format'''

    def __init__(self, config: ConfigurationManager):
        self.fov = config.get('camera.fov', 60)
        self.range = config.get('camera.range', 500)
        self.world: Optional[World] = None
        self.robot: Optional[Robot] = None

    def attach_world(self, world: World):
        self.world = world  # TODO put in init

    def attach_robot(self, robot: Robot):
        self.robot = robot

    def view(self):
        ''' Checks everything in the world and returns a string of what it sees'''

        if not self.world:
            return

        readings = []

        if ball := self.attempt_view(self.world.ball.pos):
            readings.append(f'ball,{ball.r:.4f},{ball.b:.4f}')

        for obst in self.world.obstacle_list:
            if o := self.attempt_view(obst.pos):
                readings.append(f'obst,{o.r:.4f}{o.b:.4f}')

        if goal := self.attempt_view(self.world.field.goal.center):
            readings.append(f'goal,{goal.r:.4f},{goal.b:.4f}')

        return "|".join(readings)

    def attempt_view(self, pos: Point) -> Optional[Bearing]:
        ''' Returns (range,bearing) if in the camera's view '''
        delta = Point(
            self.robot.pos.x - pos.x,
            self.robot.pos.y - pos.y
        )

        _range = round(math.sqrt(delta.x**2 + delta.y ** 2))

        if _range > self.range:
            return None

        angle = math.degrees(math.atan2( delta.x, delta.y ))
        theta = wrap180(angle - self.robot.rotation)

        if theta < -(self.fov/2) and theta > (self.fov/2):
            return None

        return Bearing(
            _range,
            theta
        )


    def obscures_point(self, obstacle:Obstacle, point:Point) -> bool:

        obst = intify(obst_rb)
        ball = intify(rb)

        if(obst[0] > ball[0]):  # obst behind ball.
            return False

        dt = int(math.degrees(math.atan2(radius, obst[0])))
        t = obst[1]
        bt = ball[1]

        #both rb are relative to robot rotation, +- ~b
        #print('obs check: ball {}, obst {}, dt {}'.format(bt,t,dt))

        if (bt > t+dt or
                bt < t-dt):
            return False

        return True
