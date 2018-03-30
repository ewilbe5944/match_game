# Imports
import pygame
import random

# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Match Game"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 30

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 175)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# match colors
DRED = (218, 67, 350)
LRED = (242, 69, 32)
DSTICK = (255, 215, 44)
LSTICK = (241, 199, 124)


def draw_match(loc):
    x = loc[0]
    y = loc[1]
    
    pygame.draw.rect(screen, LSTICK, [x+18, y+10, 5, 90], 0)
    pygame.draw.ellipse(screen, DRED, [x, y, 20, 40], 0)


#game loop
done = False

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    screen.fill(YELLOW)
    #place = [40, 60]
    #draw_match(place)





                       
    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)

# Close window on quit
pygame.quit()
