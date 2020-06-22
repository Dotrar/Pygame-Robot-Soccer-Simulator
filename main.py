from nasr.system import Configuration, Navsim
import pygame

simulator = Navsim()

pygame.init()
pygame.font.init()

screensize = width, height = 1600, 900
screen = pygame.display.set_mode(screensize, pygame.DOUBLEBUF, 32)

Navsim.attach_screen(screen)


while Navsim.running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Navsim.shutdown()

    Navsim.process()

    pygame.display.update()