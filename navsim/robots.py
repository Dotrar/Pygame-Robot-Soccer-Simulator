from typing import List, Optional

from . import ConfigurationManager
from .utils import Point
from .sensors import Camera

class Robot:
    ''' Base Robot Class'''
    def __init__(self, config: ConfigurationManager, pos: Point):
        self.size = config.get('size', 30)
        self.pos = pos
        self.rotation = 0

        self._debug = {
            'viewlines': config.get('robot.debug.viewlines', False),
            'ballline': config.get('robot.debug.ballline', False),
        }

        self.colour = pygame.Color(
            config.get('robot.colour', 'orange')
        )
        
        self.vel = Point(0,0)
        self.dt = 0
        self.camera = Camera(config)