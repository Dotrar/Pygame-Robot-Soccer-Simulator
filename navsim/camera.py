
import math, numpy as np

from navsim.helpers import *
stdn = [0,10]   #random noise

def noise(n):
    return n + np.random.normal(stdn[0],stdn[1])

class Camera(object):
    def __init__(self,conf):
        self.fov = conf['camera_fov']
        self.hfov = self.fov / 2
        self.max_range = conf['camera_max']
        self.robot = conf['robot']
        self.world = conf['world']
        


    
    def get_view(self):
        obj = []
        ball = self.check_view(self.world.ball.pos)
        
        for o in self.world.obst_list:
            obst = self.check_view(o)
            if obst:
                if ball and self.obscures(obst,self.world.obst_size+10,ball):
                    ball = None
                obj.append("obst,{r:0.4f},{b:0.4f}".format(r=obst[0],b=obst[1]))
        
        if ball:
            obj.append("ball,{r:0.4f},{b:0.4f}".format(r=ball[0],b=ball[1]))
        
        goal = self.check_view(self.world.field.goal.center)
        if goal:
            obj.append("goal,{r:0.4f},{b:0.4f}".format(r=goal[0],b=goal[1]))
            
        return "|".join(obj)
    
    #return (r,b) else False
    def check_view(self,pos):
        dx = pos[0] - self.robot.x
        dy = pos[1] - self.robot.y
        
        r = round(math.sqrt(dx**2 + dy**2))
        
        if r > self.max_range:
            return False
        
        dr = math.degrees(math.atan2(dy,dx))
        rr = self.robot.r
        
        diff = w180(dr-rr)
        
        #print("r:{},obj({},{}), diff:{}".format(
        #int(rr),int(dr),int(math.degrees(math.atan2(dy,dx))),int(diff)))
        if diff > -self.hfov and diff < self.hfov :
            return (r,diff)
        
        return False
    
    def obscures(self,obst_rb,radius,rb):
        obst = intify(obst_rb)
        ball = intify(rb)
        
        if(obst[0] > ball[0]): #obst behind ball. 
            return False
        
        dt = int(math.degrees(math.atan2(radius,obst[0])))
        t = obst[1]
        bt = ball[1]
        
        #both rb are relative to robot rotation, +- ~b
        #print('obs check: ball {}, obst {}, dt {}'.format(bt,t,dt))
        
        if ( bt > t+dt or
             bt < t-dt ):
            return False
        
        return True
