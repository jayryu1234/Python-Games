import pygame
import random
from pygame.locals import *
from pathlib import Path
invert = False
dd = Path(__file__).parent


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"images1/rocket.png").convert_alpha()
        #self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 600 /2
        self.rect[1] = 500

    def update(self):
        keys = pygame.key.get_pressed()

        # Move the square based on arrow keys
        if keys[pygame.K_LEFT]:
            self.rect[0] -= 5
        if keys[pygame.K_RIGHT]:
            self.rect[0] += 5

        


class Bullets(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        print('wahoho')
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(dd/"images1/projectile.png").convert_alpha()

        self.rect = self.image.get_rect(topleft = (xpos, ypos)) 

    def update(self):
        self.rect.y -= 1
        
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"images1/alien.png")

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 100
    def update(self):
        global invert
        if self.rect[0] >= 590:
            self.rect[1] += 10 
            invert = True
        if self.rect[0] <= 10:
            self.rect[1] += 10
            invert = False
        if invert == True:
            self.rect[0] -= 3
        if invert == False:
            self.rect[0] += 3
screen = pygame.display.set_mode((600, 600))
BACKGROUND = pygame.image.load(dd / 'images1/space.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (600, 600))
class Game():
    def __init__(self):
        pass
    def mainloop(self):
        self.keys = pygame.key.get_pressed()
        clock = pygame.time.Clock()
        enemy = Enemy()
        enemy_group = pygame.sprite.Group()
        enemy_group.add(enemy)

        player = Player()
        player_group = pygame.sprite.Group()
        player_group.add(player)

        bullet_group = pygame.sprite.Group()

        
        
    
        while True:
            self.keys = pygame.key.get_pressed()

            screen.blit(BACKGROUND, (0, 0))
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    print("gr")
                    if event.key == pygame.K_SPACE:
                        print("working")
                        bullets = Bullets(
                            player.rect.x,
                            player.rect.y
                        )      
                        
                        bullet_group.add(bullets)
                        sprite_group.add(bullets)
                if event.type == QUIT:
                    pygame.quit()
            sprite_group = pygame.sprite.Group()
            sprite_group.add(enemy)
            sprite_group.add(player)
            sprite_group.update()
            sprite_group.draw(screen)
            pygame.display.update()
            clock.tick(40)
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()