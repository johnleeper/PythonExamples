import pygame
import inspect
import random

class Treasure(pygame.sprite.Sprite):
    def __init__(self):
        super(Treasure, self).__init__() # Enables access to Sprite class methods

#        def update(self):
#            print("treasure ping")

newSprite = Treasure()

dirList = dir(newSprite)
for attr in dirList:
    print(attr)

print("%%%%%%%")
print(inspect.getmembers(Treasure, predicate=inspect.ismethod)) # needs work
