
import pygame
import math

from jtlgames.vector20 import Vector20Factory

# Initialize pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vector with Arrow")

# Create a new Vector20 class with customized screen size and scale
Vector20, draw_v20, draw_grid = Vector20Factory(screen_width, screen_height, 20)
draw_grid(screen)

# Create some vectors
v0 = Vector20(0,0)
v1 = Vector20(0, 10)
v1.rotate_ip(90)  
v2 = Vector20(3, -12)  
v3 = Vector20(-4, -2)  
v4 = Vector20(-12, 0) 
v5 = Vector20(0, 12)


start = draw_v20(screen, v0, v1)
start = draw_v20(screen, start, v2)
start = draw_v20(screen, start, v3)
start = draw_v20(screen, start, v4)
start = draw_v20(screen, start, v5)

# Update display
pygame.display.flip()

# Game loop, just pausing so you can see the screen. 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()
