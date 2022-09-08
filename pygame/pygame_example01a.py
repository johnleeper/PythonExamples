#Import and initialise pygame library
import pygame
pygame.init()

#set up the drawing window
screen = pygame.display.set_mode([500, 500])

colourdict = {"black": (0, 0, 0),
              "white": (255, 255, 255),
              "grey": (128, 128, 128),
              "light grey": (192, 192, 192),
              "blue": (0, 0, 255),
              "green": (0, 255, 0),
              "red": (255, 0, 0),
              "yellow": (255, 255, 0),
              "cyan": (0, 255, 255),
              "magenta": (255, 0, 255),
              "orange": (255, 128, 0),
              "pink": (255, 128, 128),
              "purple": (192, 0, 255),
              "indigo": (128, 0, 255),
              "amber": (255, 192, 0),
              "light blue": (128, 128, 255),
              "light green": (128, 255, 128),
              "mauve": (192, 128, 255),
              "dark blue": (0, 0, 128),
              "dark green": (0, 128, 0),
              "dark red": (128, 0, 0)
              }
              
print("Colours available include ", colourdict.keys())
bgcolour = input("Background Colour? ")
shapecolour = input("Shape Colour? ")
try:
    bgTuple = colourdict[bgcolour]
except:
    print("Background colour " + bgcolour + " does not match any known colour values")
    bgTuple = (0, 0, 0) # black used as default
try:
    shapeTuple = colourdict[shapecolour]
except:
    print("Shape colour " + shapecolour + " does not match any known colour values")
    shapeTuple = (0, 0, 0) # black used as default

#run until user asks to quit
running = True
while running:

    #Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill the background with white
    screen.fill(bgTuple)

    #Draw a solid blue circle in the centre
    pygame.draw.circle(screen, shapeTuple, (250, 250), 75)


    #flip the display, i.e. refreshes it with changes
    pygame.display.flip()

# Done! time to quit
pygame.quit()
