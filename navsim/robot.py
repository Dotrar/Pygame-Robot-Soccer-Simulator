#robot sim
import pygame

from math import *


#that, from this
from navsim.camera import Camera
from navsim.helpers import *

def wrap360(d):
    return (d+360) % 360

class Robot(object):  
    def __init__(self,config, pos = None):
        self.size = config['robot_size']
        self.AI = config['robot_AI']
        self.AI.attach_robot(self)
        self.x = pos[0] if pos is not None else config['robot_pos'][0]
        self.y = pos[1] if pos is not None else config['robot_pos'][1]
        self.r  = config['robot_rot']

        self.w = config['world']
        
        self._debug_viewlines = []
        self._debug_ballline = []
        
        
        self._colour = pygame.Color('orange')
        self._sensor_colour = pygame.Color('red')
        self._font_colour = pygame.Color('white')
        self.font = pygame.font.SysFont('consolas',12)
        
        self.show_debug = True
        self.show_AI    = True
        self.show_vectors = True
        
        self.dx = 0
        self.dy = 0
        self.dr = 0
        
        self.logger = config['console']

        config['console'].write('Robot Created!')
        config['robot'] = self
        self.camera = Camera(config)
    def log(self,s):
        self.logger.write(s)
    def view(self,world):
        #find range bearing for each object
        #send to AI
        #ai |id,range,bearing|
        return self.camera.get_view()
    
    def reposition(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        
    def update(self,dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.r = wrap360(self.r + self.dr * dt)
        self.pos = (int(self.x),int(self.y),int(self.r))  #non-writable tuple but makes calls easier
        x = self.x
        y = self.y
        s = self.size
        r = self.r
        pi = 3.141526
        self._tri_points = ((x+(s*cos(radians( 60+r))),y+(s*sin(radians( 60+r)))),
                            (x+(s*cos(radians(180+r))),y+(s*sin(radians(180+r)))),
                            (x+(s*cos(radians(300+r))),y+(s*sin(radians(300+r)))))

        if self.AI.ball_possession:
            self.w.ball.x = x+(s*cos(radians(r)))
            self.w.ball.y = y+(s*sin(radians(r)))
        
    #call AI subroutines
    def act(self,readout):
        self._debug_viewlines.clear()
        self._debug_ballline = None
        
        # ###############################
        self.AI.prepare(self.pos)
        
        if readout:
            #prep the fancy lines
            self.prepare_debug(readout)
            #process view from current camera
            self.AI.receive_readout(readout)
            
        #process data we have, forward any data here.
        self.AI.process()
        #figure out the action
        dx,dy,dr = self.AI.action()
        
        #1:1 mapping (this is a simulation afterall)
        #here is where you'd put the motor translations
        self.dx = dx
        self.dy = dy
        self.dr = dr
        
        # ###############################
   
    def toggleAI(self):
        if self.AI is not None:
            en = self.AI.enabled = not self.AI.enabled
            return 'AI Started' if en else 'AI Stopped'
        else:
            return 'no AI loaded'
    

    def draw(self,surface):
        #position
        tex = self.font.render('({x},{y})r{r}'.format(
            x=int(self.x),y=int(self.y),r=int(w180(self.r))
            ),True,self._font_colour)
        
        #robot triangle (visualise front)
        position = pygame.draw.polygon(surface,self._colour,self._tri_points)
        pygame.draw.line(surface,pygame.Color('red'),self._tri_points[0],self._tri_points[2],3)
        
        #overlay debug:
        if self.show_debug:
            self.debug_draw(surface)
        if self.show_AI:
            self.draw_ai(surface)
        if self.show_vectors:
            self.draw_vectors(surface)
        
        #position text above all.
        surface.blit(tex,position)
    
    def debug_draw(self,surface):
        colour_debug = pygame.Color('blue')
        #debug visual routines
        
        #circle aroudn robot for collision
        pygame.draw.circle(surface,pygame.Color('yellow'),self.pos[0:2],self.size,1)
        
        #camera view:
        
        #outlines:
        m = self.camera.max_range
        cr,ch,fov = self.r, self.camera.hfov, self.camera.fov+1
        x,y = self.x, self.y
        o1 = (x+m*cos(radians(cr+ch)),y+m*sin(radians(cr+ch)))
        o2 = (x+m*cos(radians(cr-ch)),y+m*sin(radians(cr-ch)))
        o3 = (x+ 0.3*m*cos(radians(cr)),y+ 0.3*m*sin(radians(cr)))
        #arc
        arc_rect = pygame.Rect(0,0,m*2,m*2) # build a giant square
        arc_rect.center = self.pos[0:2] #center on robot
        arc_b = cr + ch
        
        #negative arc values, not even sure why
        pygame.draw.arc(surface,colour_debug,arc_rect,-radians(arc_b),-radians(arc_b - fov),1)
        pygame.draw.line(surface,colour_debug,self.pos[0:2],o1)
        pygame.draw.line(surface,colour_debug,self.pos[0:2],o2)
        pygame.draw.line(surface,colour_debug,self.pos[0:2],o3)
        
        if self._debug_ballline:
            r,b = self._debug_ballline[0],self._debug_ballline[1]
            xpos =(x+r*cos(radians(b)),y+r*sin(radians(b)))
            pygame.draw.line(surface,pygame.Color('olivedrab'),self.pos[0:2],xpos,5)
            
        for line in self._debug_viewlines:
            r,b = line[0],line[1]
            xpos =[x+r*cos(radians(b)),y+r*sin(radians(b))]
            pygame.draw.line(surface,pygame.Color('maroon'),self.pos[0:2],xpos,2)
            
            xpos[1] -= 20
            surface.blit(self.font.render('Range {} Bearing {}'.format(
                int(r), int(w180(b-self.r))),True,pygame.Color('yellow')),xpos)
            
    def draw_ai(self,surface):
        if self.AI.ball:
            tex_ball = self.font.render('{} ball'.format(self.AI.ball),
                                        True,self._font_colour)
            surface.blit(tex_ball,self.AI.ball)
            
            pygame.draw.line(surface,pygame.Color('white'),self.pos[0:2],self.AI.ball)
        
        if self.AI.goal:
            t = self.font.render('{} goal'.format(self.AI.goal),
                                         True,self._font_colour)
            surface.blit(t,self.AI.goal)
            pygame.draw.line(surface,pygame.Color('white'),self.pos[0:2],self.AI.goal)
            
        for e in self.AI.map:
            gx,gy = e
            re = (gx - self.x, gy - self.y)
            t = self.font.render('{} obst'.format(intify(re)),
                                 True,self._font_colour)
            surface.blit(t,e)
            pygame.draw.line(surface,pygame.Color('white'),self.pos[0:2],e)
            
    def draw_vectors(self,surface):
        #draw as histogram
        
        window = pygame.Rect(0,0,360,100)
        pygame.draw.rect(surface,pygame.Color('white'),window)
        for idx in range(360):
            x = idx
            v = int(w360(self.r+180+idx))
            y = self.AI.vectors[v] / 100
            
            if y < 0:
                c = pygame.Color('red')
            else:
                c = pygame.Color('green')
            pygame.draw.line(surface,c,(x,50),(x,50-y))
            

    def prepare_debug(self,readout):
        readout = readout.split('|')
        for reading in readout:
            if not reading:
                break
            idx,rx,bx = reading.split(',')
            rb = r,b = float(rx),float(bx)+self.r
            if idx == 'ball':
                self._debug_ballline = rb
            elif idx == 'obst':
                self._debug_viewlines.append(rb)        
