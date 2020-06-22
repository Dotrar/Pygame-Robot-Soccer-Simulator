''' Objects module with simulation elements
'''
from typing import List, cast, Tuple, Optional
from collections import namedtuple
import logging
import pygame  # type:ignore

from . import ConfigurationManager
from .utils import Point, Rect, random_position


class Console(object):
    ''' console object for writing text on the screen'''
    log = logging.getLogger(__name__)

    def __init__(self, config: ConfigurationManager, show=True):
        self.bg_col = pygame.Color(
            config.get('console.background', 'grey')
        )
        self.fg_col = pygame.Color(
            config.get('console.foreground', 'black')
        )
        self.alpha = config.get('console.alpha', 128)

        rect: str = cast(str, config.get('console.rect', '10,10,800,400'))

        try:
            self.rect = pygame.Rect([int(x) for x in rect.split(',')])
        except ValueError:
            self.rect = pygame.Rect(10, 10, 800, 400)

        height = self.rect.height

        font: List[str] = cast(str, config.get(
            'console.font', 'consolas 16')).strip().split()

        try:
            face, size = font[0], int(font[1])
        except (ValueError, KeyError):
            face = 'consolas'
            size = 16

        self.font = pygame.font.SysFont(face, size)

        self._fontsize = size
        self._nlines = int(height / (size+1))

        self.show = show
        self.lines: List[str] = []

    def draw(self, surface):
        ''' main rendering function, accepts a surface (screen) on which to draw on '''
        if not self.show:
            return

        s = pygame.Surface(self.rect.size)
        s.set_alpha(self.alpha)
        s.fill(self.bg_col)

        rel_pos = 0
        for line in self.lines[-self._nlines:]:
            tex = self.font.render(line, True, self.fg_col)
            s.blit(tex, (self.rect[0], self.rect[1] + rel_pos))
            rel_pos = rel_pos + self._fontsize

        surface.blit(s, self.rect.topleft)

    def toggle(self):
        ''' toggle showing of the console'''
        self.show = not self.show

    def write(self, string: str) -> int:
        ''' add a line to the console '''
        self.lines.append(string)
        return len(self.lines)


class Ball:
    ''' Ball object, has velocity and deacceleration '''

    def __init__(self, config: ConfigurationManager, pos: Point):
        self.size: int = config.get('ball.size', 30)
        self.decay: int = config.get('ball.decay', 30)
        self.pos = pos
        self.vel = Point(0, 0)

    def draw(self, surface):
        ''' Renders ball object onto the surface'''
        pygame.draw.circle(
            surface,
            pygame.Color('yellow'),
            self.pos,
            self.size
        )

        pygame.draw.circle(
            surface,
            pygame.Color('orange'),
            self.pos,
            10
        )

    def update(self, dt: int):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.vel.x /= (1 + self.decay)
        self.vel.y /= (1 + self.decay)


class Field:
    ''' Field Class is the soccer field, specifies the boundaries and the goals
    '''

    def __init__(self, config):

        self.size = config.get('field.size', '1200x800').split('x')
        self.goal_size = config.get('field.goalsize', 200)

        self.rect = pygame.Rect((0, 0), self.size)
        self.rect.center = config.get('field.position', '600,400').split(',')
        self.goal = pygame.Rect(0, 0, 20, self.goal_size)

        self.goal.center = self.rect.midleft

    def update(self):
        ''' update function for the field '''
        pass

    def draw(self, surface):
        ''' drawing the field'''
        pygame.draw.rect(surface, pygame.Color('black'), self.rect, 2)
        pygame.draw.rect(surface, pygame.Color('blue'), self.goal)

    def contains_point(self, pos: Point) -> bool:
        ''' if point is in the field '''
        return self.rect.collidepoint(pos)


class World:
    def __init__(self, config: ConfigurationManager, n=0):

        self.obstacle_size = config.get('obstacle.size', 50)
        self.obstacle_list = []
        self.ball: Optional[Ball] = None
        self.configuration_manager = config
        self.field = Field(config)  # TODO componentise
        if n > 0:
            self.generate_obstacles(n)

    def generate_obstacles(self, number: int):
        ''' Generates a given number of obstacles, scattered around the world '''
        for _ in range(number):
            self.obstacle_list.append(random_position(self.field.rect))

    def place_obstacles(self, pos: Point):
        ''' places an obstacle in the given location'''
        if self.field.contains_point(pos):
            self.obstacle_list.append(pos)

    def clear_obstacles(self):
        ''' removes all obstacles from the map'''
        self.obstacle_list = []

    def place_ball(self, pos: Point):
        ''' places the ball on the map '''
        if self.field.contains_point(pos):
            self.ball = Ball(self.configuration_manager, pos)

    def clear_ball(self):
        ''' removes the ball from the map'''
        self.ball = None

    def score(self):
        '''called when player has hit a goal'''
        print('score!')

    def update(self, dt: float):
        ''' update, causes bouncing'''
        if not self.ball:
            return

        self.ball.update(dt)

        if self.ball.pos.x + self.ball.size > self.field.rect.right:
            self.ball.vel.x *= -1
        elif self.ball.pos.x - self.ball.size < self.field.rect.left:

            if y > self.field.goal.top and y < self.field.goal.bottom:
                self.score()
            else:
                self.ball.vel.x *= -1

        if self.ball.pos.y + self.ball.size > self.field.rect.bottom:
            self.ball.vel.y *= -1
        elif self.ball.pos.y - self.ball.size < self.field.rect.top:
            self.ball.vel.y *= -1

    def draw(self, surface):
        '''rendering function for world '''
        self.field.draw(surface)

        for obst in self.obstacle_list:
            pygame.draw.circle(
                surface,
                pygame.Color('black'),
                obst,
                self.obstacle_size
            )
            pygame.draw.circle(
                surface,
                pygame.Color('white'),
                obst,
                5
            )
        if self.ball:
            self.ball.draw(surface)
