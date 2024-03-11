import pygame
import sys
import math
import random
import json
# Initialize Pygame
pygame.init()
from fog import Fog
from loading_scene import LoadingScene

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define text properties
FONT_SIZE = 50
FADE_SPEED = 1
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()




def run_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)

    current_scene =LoadingScene(screen)

    while current_scene:
        current_scene = current_scene.run()

if __name__ == "__main__":
    run_game()
