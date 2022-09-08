import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE)


# Minimal pygame program, just sets up display,
# maintains it and allows user to quit
screen = pygame.display.set_mode([600, 600])
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    pygame.display.flip()

pygame.quit()
