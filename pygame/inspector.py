import pygame
import inspect
import random

class Treasure(pygame.sprite.Sprite):
    def __init__(self):
        super(Treasure, self).__init__() # Enables access to Sprite class methods
        self.score = 10
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((0, 125, 0))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, 10),
                    random.randint(0, 10),
                )
            )
        self.speed = 5
        #print("treasuer created") # diagnostic

        def update(self):
            print("treasure ping")
            self.rect.move_ip(self.speed, 0)
            if self.rect.right < 0:
                self.kill()

newSprite = Treasure()
inspect.getmembers(Treasure, predicate=inspect.ismethod)
dirList = dir(newSprite)
for attr in dirList:
    print(attr)
