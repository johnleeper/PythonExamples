#Import and initialise pygame library
import pygame

from pygame.locals import (KEYDOWN, K_ESCAPE)

pygame.init()

#set up the drawing window
screen = pygame.display.set_mode([500, 500])

#run until user asks to quit
running = True
xPosition = 100
while running:

    #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    #Fill the background with white
    screen.fill((255, 255, 255))

    #Draw a solid blue circle in the centre
    pygame.draw.circle(screen, (0, 0, 255), (xPosition, 250), 75)


    #flip the display
    pygame.display.flip()

    xPosition += 1  # Display how quickly the program loops
    if xPosition > 600: # Keeps it looping across screen
        xPosition = -50

# Done! time to quit
pygame.quit()
