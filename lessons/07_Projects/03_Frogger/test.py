import pygame
from pathlib import Path
pygame.init()
dd = Path(__file__).parent
# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("180 Degree Flip Example")

# Load an image (replace "your_image.png" with your actual image file)
try:
    original_image = pygame.image.load(dd/"images/frog.png").convert_alpha()
except pygame.error:
    print("Error loading image. Please ensure 'your_image.png' exists in the same directory.")
    pygame.quit()
    exit()

# Get the rectangle of the original image for positioning
original_rect = original_image.get_rect()
original_rect.center = (screen_width // 4, screen_height // 2)

# Perform the 180-degree flip
flipped_image = pygame.transform.flip(original_image, True, True)
flipped_rect = flipped_image.get_rect()
# flipped_rect.center = (screen_width * 3 // 4, screen_height // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fill background with white

    # Blit the original and flipped images
    screen.blit(original_image, original_rect)
    screen.blit(flipped_image, flipped_rect)

    pygame.display.flip()

pygame.quit()