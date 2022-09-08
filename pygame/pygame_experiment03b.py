import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE)

#Minimum program to get a sprite on screen
class Shark(pygame.sprite.Sprite):
    def __init__(self):
        super(Shark, self).__init__()
        sharkPNG = pygame.image.load("shark_sprite01.png").convert_alpha()
        self.image = sharkPNG
        #self.surface = self.image  ## Also works without surface
        # currently no rectangle needed


screen = pygame.display.set_mode([600, 600])
running = True
sharkSprite = Shark()
count = 0
xAxis = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    screen.fill((190, 190, 190))
    xAxis -= 0.1    # xAxis is float but converts to int where needed
    if xAxis < -20: # returns sprite back to right edge
        xAxis = 600
    screen.blit(sharkSprite.image, [xAxis, 200])
    # what is transferred and where on the screen
    pygame.display.flip()

pygame.quit()
