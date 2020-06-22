''' Objects module with simulation elements
'''
from typing import List, cast
import logging
import pygame  # type:ignore

from . import ConfigurationManager


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
    def __init__(self, config, pos=None):
        self.size = config.get('ball.size', 30)
        self.decay = config['ball_decay']
        self.x = pos[0] if pos is not None else config['ball_pos'][0]
        self.y = pos[1] if pos is not None else config['ball_pos'][1]
        self.pos = (self.x, self.y)
        self.dx = 0
        self.dy = 0
        pass

    def draw(self, surface):
        p = (int(self.x), int(self.y))
        pygame.draw.circle(surface, pygame.Color('yellow'), p, self.size)
        pygame.draw.circle(surface, pygame.Color('orange'), p, 5)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.pos = (self.x, self.y)
        self.dx /= (1 + self.decay)
        self.dy /= (1 + self.decay)
        pass


class Field:
    def __init__(self, config):

        self.size = s = config['field_size']
        self.goal_size = g = config['goal_size'] if 'goal_size' in config else 40
        scr = config['screen_size']

        self.rect = pygame.Rect((0, 0), s)
        self.rect.center = (scr[0]/2, scr[1]/2)

        self.goal = pygame.Rect(0, 0, 20, g)

        self.goal.center = self.rect.midleft

    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color('black'), self.rect, 2)
        pygame.draw.rect(surface, pygame.Color('blue'), self.goal)

    def contains_point(self, pos):
        return self.rect.collidepoint(pos)

    def top(self):
        return self.rect[1]

    def bottom(self):
        return self.rect[1]+self.rect[3]

    def left(self):
        return self.rect[0]

    def right(self):
        return self.rect[0] + self.rect[2]


class World:
    log = logging.getLogger(__name__)

    def __init__(self, config, n=0):

        self.obstacle_size = config.get('obstacle.size', 50)
        self.obstacle_list = []
        if n is not 0:
            generate_obst(n)
            self.console.write("Made {0} objects".format(n))

        self.console.write("Field: {0}".format(self.field.rect.size))
        self.console.write("Screen: {0}".format(config['screen_size']))
        config['world'] = self
        pass

    def generate_obst(self, number):
        for i in range(number):
            self.obst_list.append(randtuple(self.field.rect))

    def place_obst(self, pos):
        if self.field.contains_point(pos):
            self.obst_list.append(pos)

    def clear_obst(self):
        self.obst_list = []

    def place_ball(self, pos):
        self.ball = Ball(self.configuration, pos)

    def clear_ball(self):
        self.ball = None

    def update(self, dt):
        if self.ball is not None:
            self.ball.update(dt)

            x, y, r = self.ball.x, self.ball.y, self.ball.size

            if x+r > self.field.right():
                self.ball.dx = -abs(self.ball.dx)
            elif x-r < self.field.left():
                #GOAL condition
                if y > self.field.goal.top and (y <
                                                self.field.goal.bottom):
                    self.scored = True
                self.ball.dx = abs(self.ball.dx)
            if y+r > self.field.bottom():
                self.ball.dy = -abs(self.ball.dy)
            elif y-r < self.field.top():
                self.ball.dy = abs(self.ball.dy)

    def draw(self, surface):

        #draw field
        self.field.draw(surface)

        #each obstacle
        for each in self.obst_list:
            pygame.draw.circle(surface, pygame.Color(
                'black'), each, self.obst_size)
            pygame.draw.circle(surface, pygame.Color('white'), each, 5)

        #draw ball
        if self.ball is not None:
            self.ball.draw(surface)
