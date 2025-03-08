import pygame, random, time
from pygame.locals import *
from pathlib import Path

#VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15
BLACK = (0, 0, 0)
GROUND_WIDTH = 2 * SCREEN_HEIGHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150
score = 0

dd = Path(__file__).parent



wing = dd/'assets/audio/wing.wav'
hit = dd/'assets/audio/hit.wav'
class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.pic = pygame.image.load(dd/"assets/sprites/base.png").convert_alpha()
        self.pic = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.pic.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_offscreenprob(sprite):
    return sprite.rect[0] < -sprite[2]/2

class Bird():
    pass
class Pipe():
    pass
def main():
    pass
if __name__ == "main":
    main()

