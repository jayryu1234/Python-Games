import pygame
import random
from pygame.locals import *
from pygame import sprite
from pathlib import Path
pygame.mixer.init()
music = random.randint(1, 2)
invert = False
plus = 0
dd = Path(__file__).parent
screen = pygame.display.set_mode((600, 600))
BACKGROUND = pygame.image.load(dd / 'images1/space.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (600, 600))
column = 1
enemies = []
pygame.mixer.init()
start_time = pygame.time.get_ticks()

pygame.mixer.music.load(dd/"sounds/BGMFB_BLUUDUDE_CHASE_THEME.wav")
pygame.mixer.music.play(-1)

class Player(sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"images1/rocket.png").convert_alpha()
        #self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = self.rect.center
        self.rect[0] = 600 /2
        self.rect[1] = 480

    def update(self):
        keys = pygame.key.get_pressed()

        # Move the square based on arrow keys
        if keys[K_w] and self.rect.y >= 150:
            self.rect.y -= 3
        if keys[K_s] and self.rect.y <= 480:
            self.rect.y += 3
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= 5
        if keys[K_d] and self.rect.x < 570:
            self.rect.x += 5

        


class Bullets(sprite.Sprite):
    def __init__(self, xpos, ypos):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(dd/"images1/projectile.png").convert_alpha()

        self.rect = self.image.get_rect(topleft = (xpos + 5, ypos)) 

    def update(self):
        screen.blit(self.image, self.rect)

        self.rect.y -= 20
        
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()

class Enemy(sprite.Sprite):
    def __init__(self, num, column, edge):
        pygame.sprite.Sprite.__init__(self)
        self.type = edge
        self.image = pygame.image.load(dd/"images1/alien.png")
        self.rect = self.image.get_rect()
        self.rect[0] = num
        self.num = num
        self.og_y = 100 + column*20
        self.rect[1] = self.og_y
        self.invert = False


    def update(self):
        if self.invert == True:
                self.rect[0] -= 10
        if self.invert == False:
                self.rect[0] += 10

class enemies(sprite.Group):
    def __init__(self, columns, rows):
        sprite.Group.__init__(self)
    # def is_column_dead(self, column):
    #     return not any(self.enemies[row][column] for row in range(self.rows))
        

class Game():
    def __init__(self):
        pass
    def mainloop(self):

        last_shot_time = 0
        self.keys = pygame.key.get_pressed()
        clock = pygame.time.Clock()

        enemy_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        num = 1
  
        column = 0
        player = Player()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        sprite_group = pygame.sprite.Group()

        for _ in range(30):
            if _ == 14:
                new_enemy = Enemy(num = num*20, column = column, edge = True)
                column += 1
                num = 1
            
            else:
                new_enemy = Enemy(num = num*20, column = column, edge = False)

                num += 1
            enemy_group.add(new_enemy)


        sprite_group.add(player)

        while True:
            self.keys = pygame.key.get_pressed()

            screen.blit(BACKGROUND, (0, 0))
            
            for event in pygame.event.get():
                if self.keys[K_SPACE]:

                        # Check if enough time has passed to fire another shot
                        current_time = pygame.time.get_ticks()
                        if current_time - last_shot_time >= 100:
                            last_shot_time = current_time
                            bullets = Bullets(
                            player.rect.x,
                            player.rect.y
                        )      
                        
                            bullet_group.add(bullets)
                            sprite_group.add(bullets)
                if event.type == QUIT:
                    pygame.quit()
            


        # Move the square based on arrow keys
            

                    
            enemy_group.update()
            enemy_x = [enemy.rect.x for enemy in enemy_group]
            
            try:
                if min(enemy_x) <= 0 or max(enemy_x) >= 600:
                    for i in range(len(enemy_group)):
                        enemy_group.sprites()[i].invert = not enemy_group.sprites()[i].invert
                        enemy_group.sprites()[i].rect.y += 10
            except ValueError:
                num = 1

                for _ in range(75):
                    if _ == 0:
                        new_enemy = Enemy(num = num*20, column = column, edge = False)

                        num += 1
                    elif _ == 14:
                        new_enemy = Enemy(num = num*20, column = column, edge = True)
                        column += 1
                        num = 1
                    elif _== 29:
                        new_enemy = Enemy(num = num*20, column = column, edge = True)
                        column += 1
                        num = 1
                    elif _ == 44:
                        new_enemy = Enemy(num = num*20, column = column, edge = True)
                        column += 1
                        num = 1
                    elif _ == 59:
                        new_enemy = Enemy(num = num*20, column = column, edge = True)
                        column += 1
                        num = 1
                    else:
                         new_enemy = Enemy(num = num*20, column = column, edge = False)

                         num += 1
                    enemy_group.add(new_enemy)

            enemy_group.draw(screen)
            
            sprite_group.update()
            sprite_group.draw(screen)
            pygame.display.update()
            clock.tick(40)

            pygame.sprite.groupcollide(bullet_group, enemy_group, True, True, pygame.sprite.collide_mask)
            pygame.sprite.groupcollide(player_group, enemy_group, True, True, pygame.sprite.collide_mask)
                  
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()
