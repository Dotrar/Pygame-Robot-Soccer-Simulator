#random code for simulator
import pygame,random

from navsim.field import Field
from navsim.ball import Ball

def randtuple(rect):
    return (random.randint(rect[0],rect[0]+rect[2]),
            random.randint(rect[1],rect[1]+rect[3]))

class World(object):
    def __init__(self,config,n=0):
        self.configuration = config
        self.obst_size = config['obst_size']
        self.console = console = config['console']
        self.field = Field(config)
        self.ball = Ball(config)
        self.obst_list = []
        self.scored = True
        
        self.console.write("World created!")
        if n is not 0:
            generate_obst(n)
            self.console.write("Made {0} objects".format(n))
        
        self.console.write("Field: {0}".format(self.field.rect.size))
        self.console.write("Screen: {0}".format(config['screen_size']))
        config['world'] = self
        pass

    def generate_obst(self,number):
        for i in range(number):
            self.obst_list.append(randtuple(self.field.rect))
            
    def place_obst(self,pos):
        if self.field.contains_point(pos):
            self.obst_list.append(pos)
    def clear_obst(self):
        self.obst_list = []
        
    def place_ball(self,pos):
        self.ball = Ball(self.configuration,pos)
        
    def clear_ball(self):
        self.ball = None
        
    def update(self,dt):
        if self.ball is not None:
            self.ball.update(dt)
            
            x,y,r = self.ball.x,self.ball.y,self.ball.size
            
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
    
    def draw(self,surface):

        #draw field
        self.field.draw(surface)
        
        #each obstacle
        for each in self.obst_list:
            pygame.draw.circle(surface,pygame.Color('black'),each,self.obst_size)
            pygame.draw.circle(surface,pygame.Color('white'),each,5)
            
        #draw ball
        if self.ball is not None:
            self.ball.draw(surface)
        