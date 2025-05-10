import pygame
import random
from pygame.locals import *
from pathlib import Path

dd = Path(__file__).parent

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"images/rocket.png").convert_alpha()
        #self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 400 /6
        self.rect[1] = 300
class Enemy():
    def __init__(self):
        pass
screen = pygame.display.set_mode((400, 600))
def mainloop():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        player = Player()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        player_group.draw(screen)
        pygame.display.update()
while True:
    mainloop()
    
