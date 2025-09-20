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
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 505
        self.rect.center = self.rect.center
    def update(self, num):
        if num == 1:
            self.rect.y -= 75
        if num == 2:
            self.rect.y += 75
        if num == 3 and not self.rect.x <= 0:
            self.rect.x -= 75
        if num == 4 and not self.rect.x >= 525:
            self.rect.x += 75
        if num == 5:
            pass
        
class Car(sprite.Sprite):
    def __init__(self, column, dir):
        pygame.sprite.Sprite.__init__(self)
        self.dir = dir
        if dir == "left":
            self.image = pygame.image.load(dd/"images/carRight.png").convert_alpha()
        if dir == "right":
            self.image = pygame.image.load(dd/"images/carLeft.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        if dir == "left":
            self.rect.x = 0
        if dir == "right":
            self.rect.x = 525
        self.rect.y = column *75
        self.rect.center = self.rect.center
    def update(self):

        if self.dir == "Left":
            if self.rect.right < 0:
                self.kill()
            self.rect.x -= 10
        if self.dir == "Right":
            if self.rect.left > 525:
                self.kill()
            self.rect.x += 10
class Game():
    def __init__(self):
        pygame.init()
        self.obstacle_count = 0

    def add_obstacle(self, obstacles):
        # random.random() returns a random float between 0 and 1, so a value
        # of 0.25 means that there is a 25% chance of adding an obstacle. Since
        # add_obstacle() is called every 100ms, this means that on average, an
        # obstacle will be added every 400ms.
        # The combination of the randomness and the time allows for random
        # obstacles, but not too close together. 
        
        if random.random() < 0.5:
            x = random.randint(1, 2)
            if x == 1:
                dir = "left"
            if x == 2:
                dir = 'right'
            print(dir)
            column = random.randint(1, 3)
            obstacle = Car(dir = dir, column = column)
            obstacles.add(obstacle)
            return 1
        return 0
    
    def mainloop(self):
        last_obstacle_time = pygame.time.get_ticks()
        self.keys = pygame.key.get_pressed()
        last_hold_time = 0
        clock = pygame.time.Clock()
        obstacles = pygame.sprite.Group()
        player = Frog()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        sprite_group = pygame.sprite.Group()
        sprite_group.add(player)
        ismovin = False
        running = True
        hepressed = False
        while running:
            if pygame.time.get_ticks() - last_obstacle_time > 600:
                        last_obstacle_time = pygame.time.get_ticks()
                        self.obstacle_count += Game.add_obstacle(self, obstacles)
            obstacles.update()
            if player.rect.y <= -75:
                font = pygame.font.SysFont("Arial", 30)
                text_surface = font.render("wowieee u won :D", True, (255, 255, 255))
                screen.blit(text_surface, (100, 100))
                pygame.display.update()

            for event in pygame.event.get():
                current_time = pygame.time.get_ticks()
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and not ismovin:
                        last_hold_time = current_time
                        player_group.update(1)
                        ismovin = True
                        hepressed = True
                    elif event.key == pygame.K_s and current_time - last_hold_time >= 500:
                        last_hold_time = current_time
                        player_group.update(2)
                        hepressed = True
                        ismovin = True
                    elif event.key == pygame.K_a and not ismovin:
                        player_group.update(3)
                        ismovin = True
                        hepressed = True
                    elif event.key == pygame.K_d and not ismovin:
                        player_group.update(4)
                        ismovin= True
                        hepressed = True

                    ismovin = False
            screen.blit(BACKGROUND, (0, 0))
            start_time = pygame.time.get_ticks()
            if start_time <= 7000 and hepressed == False:
                font = pygame.font.SysFont("Arial", 30)
                controls = font.render("Controls:", True, (255, 255, 255))
                w = font.render('W = move forward', True, (255, 255, 255))
                a = font.render('A = move left', True, (255, 255, 255))
                s = font.render('S = move back (500 ticks cooldown)', True, (255, 255, 255))
                d = font.render('D = move right', True, (255, 255, 255))
                screen.blit(controls, (0, 100))
                screen.blit(w, (0, 140))
                screen.blit(a, (0, 180))
                screen.blit(s, (0, 220))
                screen.blit(d, (0, 260))

            obstacles.draw(screen)
            
            sprite_group.update(5)
            sprite_group.draw(screen)
            pygame.display.update()
            clock.tick(40)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()

