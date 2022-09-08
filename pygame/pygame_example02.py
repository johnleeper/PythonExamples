import pygame

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
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect()

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
    def __init__(self):
        super(Enemy, self).__init__() # Enables access to Sprite class methods
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH +100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
        self.speed = random.randint(5, 20)
        #print("enemy created") # diagnostic

        def update(self):
            self.rect.move_ip(self.speed, 0)
            if self.rect.right < 0:
                self.kill()

#initialize pygame
pygame.init()

#Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT +1
pygame.time.set_timer(ADDENEMY, 250) # parameters are event name/number, millisecs
player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
    screen.fill((255, 255, 255))
    surf = pygame.Surface((50, 50))
    #surf.fill((0, 0, 255))
    #rect = surf.get_rect()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    #print("Hello")
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # This line says "Draw surf onto the screen at the center"
    screen.blit(surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) # blit is Block Transfer
    screen.blit(player.surf, player.rect)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    
    pygame.display.flip() # essential for getting things to display

pygame.quit()
