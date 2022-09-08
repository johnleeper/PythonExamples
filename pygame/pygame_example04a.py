import pygame
import pygame.sprite

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    )
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        playerPNG = pygame.image.load("diver_sprite01.png").convert_alpha()
        super(Player, self).__init__()
        self.image = playerPNG
        self.surface = self.image
        self.rect = self.image.get_rect(center = (400, 300))
        self.mask = pygame.mask.from_surface(self.surface)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT        

class Enemy(pygame.sprite.Sprite):
    count = 0
    def __init__(self):
        enemyPNG = pygame.image.load("shark_sprite01.png").convert_alpha()
        super(Enemy, self).__init__() # Enables access to Sprite class methods
        self.image = enemyPNG
        self.surface = self.image
        self.rect = self.surface.get_rect(
            center=(SCREEN_WIDTH,
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
        self.mask = pygame.mask.from_surface(self.surface)
        self.speed = random.randint(5, 20)
        #print("enemy created") # diagnostic

    def update(self):
#        print("enemy pong")
        self.count +=1
        if self.count == 8:
            self.rect.move_ip(-1, 0)
            self.count = 0
#            print("ping")
        if self.rect.right < 0 or self.rect.right > SCREEN_WIDTH+70:
            print("shark at ", self.rect.right)
            self.kill()

class Treasure(pygame.sprite.Sprite):
    def __init__(self):
        super(Treasure, self).__init__() # Enables access to Sprite class methods
        self.score = 10
        self.surface = pygame.Surface((20, 10))
        self.surface.fill((0, 125, 0))
        self.rect = self.surface.get_rect(
            center=(random.randint(0, SCREEN_WIDTH +10),
                    random.randint(0, SCREEN_HEIGHT +10),
                )
            )
        self.speed = random.randint(5, 20)
        #print("treasuer created") # diagnostic

#    def update(self):
#        print("treasure ping")
#        self.rect.move_ip(self.speed, 0)
#        if self.rect.right < 0:
#            self.kill()    

#initialize pygame
pygame.init()

#Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT +1
pygame.time.set_timer(ADDENEMY, 2500) # parameters are event name/number, millisecs
ADDTREASURE = pygame.USEREVENT +2
pygame.time.set_timer(ADDTREASURE, 500)
player = Player()

enemies = pygame.sprite.Group()
treasures = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
timeSurvived = 0
treasureScore = 0

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
            print("QUIT event")
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDTREASURE:
            new_treasure = Treasure()
            treasures.add(new_treasure)
            all_sprites.add(new_treasure)
            #print("new treasure at: ", new_treasure)
        
    screen.fill((125, 255, 255))

    for entity in all_sprites:
        screen.blit(entity.surface, entity.rect)
        #print(entity)
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
        print("Player Killed")

    if pygame.sprite.spritecollideany(player, treasures):
        collectedTreasure = pygame.sprite.spritecollide(player, treasures, True)
        for treasure in collectedTreasure:
            treasureScore += treasure.score
            treasure.kill()
            
        
# blit is Block Transfer
    screen.blit(player.surface, player.rect)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    treasures.update()
    timeSurvived += 0.001
    
    pygame.display.flip() # essential for getting things to display

pygame.quit()
print("Time Survived: ", timeSurvived)
print("Treasure Score: ", treasureScore)
