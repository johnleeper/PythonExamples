import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE)

#Minimum program to get a sprite on screen
class Shark(pygame.sprite.Sprite):
    def __init__(self):
        super(Shark, self).__init__()
        sharkPNG = pygame.image.load("shark_sprite01.png").convert_alpha()
        self.image = sharkPNG
        self.surface = self.image
        # currently no rectangle needed


screen = pygame.display.set_mode([600, 600])
running = True
sharkSprite = Shark()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    screen.fill((190, 190, 190))
    screen.blit(sharkSprite.surface, [200, 200])
    # what is transferred and where on the screen
    pygame.display.flip()

pygame.quit()
