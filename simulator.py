'''
Main File
'''
from ai.nasr import Nasr
import pygame  # type: ignore
from typing import Any

from navsim import ConfigurationManager
from navsim.objects import Console, World
from navsim.robots import Robot

''' Some different ai options '''
# from ai.ekf import ekf

'''---------------------------'''

pygame.init()
pygame.font.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, 32)

config = ConfigurationManager(None)
console = Console(config)
world = World(config)
robot = Robot(config)

ai = Nasr()

# any further here

robot.attach_AI(ai)


gen_rand = False
placed = False
ang = 0


header = '''NavSim - Navigation Simulator
    Written by D.West (WSU, QUT)
    dre.west@outlook.com
    --------------------
    help:
    .   g       :place ball
    .   click   :place obstruction
    .   r-click :place robot (hold=rotate)
    .   [space] :play/stop
    .   [tab]   :show/hide console
    .   [1,2,3] :debug showing
    .   [bksp]  :reset simulation
    .   h       :print this header
    '''

console.write(header)


def check_key(event: Any, key: int) -> bool:
    return (event.type == pygame.KEYUP and event.key == key)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                world.place_obst(pygame.mouse.get_pos())
            if event.button == 3:
                placed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if not placed:
                    #robot = Robot(configuration, pos = pygame.mouse.get_pos())
                    robot.reposition(pygame.mouse.get_pos())
                    placed = True

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[2]:
                r = (robot.x, robot.y)
                p = pygame.mouse.get_pos()
                robot.r = math.degrees(math.atan2(p[1]-r[1], p[0]-r[0]))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                world.clear_obst()
            elif event.key == pygame.K_s:
                console.write(robot.toggleAI())
            elif event.key == pygame.K_TAB:
                console.toggle()
            elif event.key == pygame.K_g:
                world.place_ball(pygame.mouse.get_pos())
            elif event.key == pygame.K_d:
                robot.show_debug = not robot.show_debug
                console.write(
                    "Debug " + ("shown" if robot.show_debug else "hidden"))
            elif event.key == pygame.K_a:
                robot.show_AI = not robot.show_AI
                console.write("AI " + ("shown" if robot.show_AI else "hidden"))
            elif event.key == pygame.K_v:
                robot.show_vectors = not robot.show_vectors
                console.write(
                    "VFF " + ("shown" if robot.show_vectors else "hidden"))
            elif event.key == pygame.K_c:
                robot.AI.map.clear()
                robot.AI.vectors.fill(0)
                robot.AI.ball = None
                robot.AI.goal = None

                console.write('cleared AI map')
            elif event.key == pygame.K_h:
                for line in h.split('\n'):
                    console.write(line)

            elif event.key == pygame.K_r:
                gen_rand = True
            elif gen_rand and (event.key - 48) in range(10):
                world.generate_obst(event.key-48)

            elif event.key == pygame.K_BACKSPACE:
                # huge reset
                configuration['robot_AI'] = NASR({
                    'sensor_range': 600,
                })
                console = Console(configuration)

                world = World(configuration)

                # camera is always created last, which is in robot
                robot = Robot(configuration)

                gen_rand = False
                placed = False
                ang = 0

                console.write(
                    'NASR - Not a Soccer Robot. AI design by D.West n9142461 - dre.west@connect{...}')
                for line in h.split('\n'):
                    console.write(line)

    world.update(1)
    robot.update(1)  # update robot after world for ball update

    readout = robot.view(world)

    robot.act(readout)

    screen.fill(pygame.Color('darkgreen'))

    world.draw(screen)
    robot.draw(screen)
    console.draw(screen)

    pygame.display.update()
