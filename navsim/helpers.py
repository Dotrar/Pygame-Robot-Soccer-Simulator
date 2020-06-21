
from math import *

__cmpixscale = 10
__similarity_limit = 30
def cm(cm):
    #return the cm representation in pixels
    return int(cm * __cmpixscale)

def to_cm(pix):
    return pix / __cmpixscale

def floatify(list):
    ret = []
    for f in list:
        ret.append(float(f))
    return ret

def intify(list):
    ret = []
    for f in list:
        ret.append(int(f))
    return ret

def err_tuple(t1,t2):
    return abs(t1[0]-t2[0]) + abs(t1[1]-t2[1])

def find_similar(obj,list):
    err = []
    for o in list:
        err.append(err_tuple(obj,o))
    if [e for e in err if e < __similarity_limit]:
        return err.index(min(err))
    return None

def pol2rect(rb):
    r,b = rb
    return r*cos(radians(b)), r*sin(radians(b))
def rect2pol(xy):
    x,y = xy
    return sqrt(x**2 + y**2),degrees(atan2(y,x))

def in_arc(pos, rel, ang, half_fov,range):

    dx = pos[0] - rel[0]
    dy = pos[1] - rel[1]
    
    r = round(sqrt(dx**2 + dy**2))
    
    if r > range:
        return False
    
    diff = w180(degrees(atan2(dy,dx))- ang)
    
    #print("r:{},obj({},{}), diff:{}".format(
    #int(rr),int(dr),int(math.degrees(math.atan2(dy,dx))),int(diff)))
    if diff > - half_fov and diff < half_fov :
        return (r,diff)
    
    return False


def w360(d):
    return (d+360) % 360
def w180(d):
    return (d+180)%360 - 180

