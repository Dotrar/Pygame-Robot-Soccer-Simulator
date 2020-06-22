

import pygame

class Field(object):
    def __init__(self,config):

        self.size = s = config['field_size']
        self.goal_size = g = config['goal_size'] if 'goal_size' in config else 40
        scr = config['screen_size']

        self.rect = pygame.Rect((0,0),s)
        self.rect.center = (scr[0]/2,scr[1]/2)

        self.goal = pygame.Rect(0,0,20,g)

        self.goal.center = self.rect.midleft

    def update(self):
        pass
    def draw(self,surface):
        pygame.draw.rect(surface,pygame.Color('black'),self.rect,2)
        pygame.draw.rect(surface,pygame.Color('blue'),self.goal)

    def contains_point(self,pos):
        return self.rect.collidepoint(pos)

    def top(self):
        return self.rect[1]
    def bottom(self):
        return self.rect[1]+self.rect[3]
    def left(self):
        return self.rect[0]
    def right(self):
        return self.rect[0] + self.rect[2]
