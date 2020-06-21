import pygame

class Ball(object):
    def __init__(self,config,pos = None):
        self.size = config['ball_size']
        self.decay = config['ball_decay']
        self.x = pos[0] if pos is not None else config['ball_pos'][0]
        self.y = pos[1] if pos is not None else config['ball_pos'][1]
        self.pos = (self.x,self.y)
        self.dx = 0
        self.dy = 0
        pass
    def draw(self,surface):
        p = (int(self.x),int(self.y))
        pygame.draw.circle(surface,pygame.Color('yellow'),p,self.size)
        pygame.draw.circle(surface,pygame.Color('orange'),p,5)        

    def update(self,dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.pos = (self.x,self.y)
        self.dx /= (1+ self.decay)
        self.dy /= (1+ self.decay)
        pass
    