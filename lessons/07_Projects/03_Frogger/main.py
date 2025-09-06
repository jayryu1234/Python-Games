import pygame
import random
from pygame.locals import *
from pygame import sprite
from pathlib import Path
pygame.mixer.init()
music = random.randint(1, 2)
invert = False
plus = 0
forever = False
dd = Path(__file__).parent
screen = pygame.display.set_mode((600, 600))
BACKGROUND = pygame.image.load(dd / 'images/frogger_road_bg.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (600, 600))
start_time = pygame.time.get_ticks()

class Frog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"images/frog.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        #self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = self.rect.center
    def update(self):
        self.keys = pygame.key.get_pressed()
      
        #print('update')
        # Move the square based on arrow keys
        if self.keys[K_w]:
            print('andrew is the worst teacher yayayayay')
            self.rect.y -= 30
        if self.keys[K_s]:
            self.rect.y += 30
            print('andrew is the worst teacher yayayayay')
        if self.keys[K_a]:
            self.rect.x -= 30
            print('andrew is the worst teacher yayayayay')
        if self.keys[K_d]:
            self.rect.x += 30
            print('andrew is the worst teacher yayayayay')

class Game():
    def __init__(self):
        pass
    def mainloop(self):
        self.keys = pygame.key.get_pressed()
        
        clock = pygame.time.Clock()

        enemy_group = pygame.sprite.Group()
        player = Frog()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        sprite_group = pygame.sprite.Group()
        sprite_group.add(player)

        while True:
            self.keys = pygame.key.get_pressed()
            screen.blit(BACKGROUND, (0, 0))

            enemy_group.draw(screen)
            
            sprite_group.update()
            sprite_group.draw(screen)
            pygame.display.update()
            clock.tick(40)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()

