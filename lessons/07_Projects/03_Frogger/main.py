import pygame
import random
from pygame.locals import *
from pygame import sprite
from pathlib import Path
dd = Path(__file__).parent
screen = pygame.display.set_mode((600, 600))
BACKGROUND = pygame.image.load(dd / 'images/frogger_road_bg.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (600, 600))

class Frog(sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"images/frog.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        #self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 505
        self.rect.center = self.rect.center
    def update(self, num):
        if num == 1:
            self.rect.y -= 75
        if num == 2:
            self.rect.y += 75
        if num == 3:
            self.rect.x -= 75
        if num == 4:
            self.rect.x += 75
        if num == 5:
            pass
        

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
        ismovin = False
        running = True
        while running:
            if player.rect.y <= -75:
                font = pygame.font.SysFont("Arial", 30)
                text_surface = font.render("wowieee u won :D", True, (255, 255, 255))
                screen.blit(text_surface, (100, 100))
                pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and not ismovin:
                        player_group.update(1)
                        ismovin = True
                    elif event.key == pygame.K_s and not ismovin:
                        player_group.update(2)
                        ismovin = True
                    elif event.key == pygame.K_a and not ismovin:
                        player_group.update(3)
                        ismovin = True
                    elif event.key == pygame.K_d and not ismovin:
                        player_group.update(4)
                        ismovin= True

                    ismovin = False
                    print('andrew is the worst teacher yayayayay')
            screen.blit(BACKGROUND, (0, 0))

            enemy_group.draw(screen)
            
            sprite_group.update(5)
            sprite_group.draw(screen)
            pygame.display.update()
            clock.tick(40)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()

