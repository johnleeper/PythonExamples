import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE)


# Background colour changer
screen = pygame.display.set_mode([600, 600])
running = True
red = 255
green = 255
blue = 255
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    red += 0.011
    if red > 255:
        red = 0
    green += 0.02
    if green > 255:
        green = 0
    blue += 0.03
    if blue > 255:
        blue = 0
    screen.fill((int(red), int(green), int(blue)))
    pygame.display.flip()

pygame.quit()
