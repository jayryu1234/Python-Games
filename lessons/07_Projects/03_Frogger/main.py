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
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 520
        self.rect.center = self.rect.center
    def oof(self):
        self.image = pygame.image.load(dd/"images/explosion1.gif").convert_alpha()
    def update(self, num):
        if num == 1 and self.rect.y >= -75:
            self.rect.y -= 75
        if num == 2 and self.rect.y <= 520:
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

        self.image = pygame.transform.scale(self.image, (75, 75))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        if dir == "left":
            self.rect.x = 0
        if dir == "right":
            self.rect.x = 525
        self.rect.y =520-  column *75
        self.rect.center = self.rect.center
    def update(self):

        if self.dir == "left":
            if self.rect.right > 525:
                 self.kill()

            self.rect.x += 5
        if self.dir == "right":
            if self.rect.left < 0:
                self.kill()
            self.rect.x -= 5
class Game():
    def lvl_up(self):
        pass
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
        
            x = random.randint(1, 2)
            if x == 1:
                dir = "left"
            if x == 2:
                dir = 'right'
            column = random.randint(1, 5)
            obstacle = Car(dir = dir, column = column)
            obstacles.add(obstacle)
            return 1
    
    def mainloop(self):
        waiting_time = 0
        last_complete_time = pygame.time.get_ticks()
        front = False
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
        bad_boi = False
        level = 1
        true_lvl = level
        good_boi = True
        game_complete = False
        game_over = False
        hepressed = False
        aa= 0
        b= 0
        c= 0
        while running:
            while not game_over and not game_complete:
                if level == "car hell":
                        
                        if pygame.time.get_ticks() - last_obstacle_time > 1000:

                            for i in range(4):
                                    self.obstacle_count += Game.add_obstacle(self, obstacles)
                                    last_obstacle_time = pygame.time.get_ticks()
                elif level == "waiting game":
                        if good_boi == True:
                            if pygame.time.get_ticks() - last_obstacle_time > 1200:
                                last_obstacle_time = pygame.time.get_ticks()
                                self.obstacle_count += Game.add_obstacle(self, obstacles)
                        else:
                            for i in range(10):
                                self.obstacle_count += Game.add_obstacle(self, obstacles)
                elif level >= 5:        
                    if pygame.time.get_ticks() - last_obstacle_time > 350:
                            last_obstacle_time = pygame.time.get_ticks()
                            self.obstacle_count += Game.add_obstacle(self, obstacles)
                elif pygame.time.get_ticks() - last_obstacle_time > 400 - level*20:
                            last_obstacle_time = pygame.time.get_ticks()
                            self.obstacle_count += Game.add_obstacle(self, obstacles)
                
                obstacles.update()
                if player.rect.y >= 520 and front == True:
                    game_complete = True
                    pygame.display.update()
                if player.rect.y <= -75:
                    font = pygame.font.SysFont("Arial", 30)

                    if level == "waiting game" and pygame.time.get_ticks() - last_complete_time < waiting_time:
                        text_surface = font.render("bad boiii", True, (255, 255, 255))
                        good_boi = False
                    else:
                        text_surface = font.render("go backk", True, (255, 255, 255))
                    
                    front = True
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
                font = pygame.font.SysFont("Arial", 30)
                if level == 1:
                    prompt = "mild"
                if level == 2:
                    prompt = "okay"
                if level == 3:
                    prompt = "a bit dangerous"
                if level == 4:
                    prompt = "SCARY :0"
                if level == 5:
                    prompt = "aw hell naw"
                if level == "car hell":
                    prompt = "???"
                # if level == 7:
                #     prompt = "new york style 💀"
                if level == "waiting game":
                    prompt = 'huh'
                if bad_boi == True:
                    prompt = 'BAD BOI'
                car_cd = font.render(f"cars trafficking level: {prompt}", True, (255, 255, 255))
                if level == 6:
                    prompt2 = "???"
                if level == "waiting game":


                    if not bad_boi == True:
                        prompt2 = "this ez level for break time"
                    else:
                        prompt2 = "GRR GRR PATAPIM"
                    
                else:
                    prompt2 = level
                level_text = font.render(f'Level: {prompt2}', True, (255, 255, 255))
                waiting_text = font.render(f'{waiting_time}', True, (255, 255, 255))
                if level == "waiting game" or level == "car hell":
                    aa += 1
                    b += 2
                    c += 3
                    if aa >= 255:
                        aa = 0
                    if b >= 255:
                        b = 0
                    if c >= 255:
                        c= 0
                    special_level = font.render(f'SPECIAL LEVEL!!!', True, (aa, b, c))
                    
                screen.blit(BACKGROUND, (0, 0))
                screen.blit(level_text, (25, 25))
                screen.blit(car_cd, (25, 65))
                try:
                    if level == "waiting game":
                        screen.blit(waiting_text, (25, 135))
                except UnboundLocalError:
                    pass
                try:
                    if level == "car hell":
                        screen.blit(special_level, (25, 100))
                except UnboundLocalError:
                    pass
                start_time = pygame.time.get_ticks()
                if start_time <= 7000 and hepressed == False:
                    controls = font.render("Controls:", True, (255, 255, 255))
                    w = font.render('W = move forward', True, (255, 255, 255))
                    a = font.render('A = move left', True, (255, 255, 255))
                    s = font.render('S = move back (500 ticks cooldown)', True, (255, 255, 255))
                    d = font.render('D = move right', True, (255, 255, 255))
                    win = font.render('to win, go to the top and go baacckk', True, (255, 255, 255))
                    screen.blit(controls, (0, 100))
                    screen.blit(w, (0, 140))
                    screen.blit(a, (0, 180))
                    screen.blit(s, (0, 220))
                    screen.blit(d, (0, 260))
                    screen.blit(win, (0, 300))

                obstacles.draw(screen)

                collider = pygame.sprite.groupcollide(player_group, obstacles, False, False)
                if collider:
                    player.oof()
                    game_over = True

                sprite_group.update(5)
                sprite_group.draw(screen)
                pygame.display.update()
                clock.tick(40)
            while game_complete:
                pygame.event.get()
                font = pygame.font.SysFont("Arial", 30)
                text_surface = font.render("ta da! u win", True, (255, 255, 255))
                e = font.render('press the "e" key to continue', True, (255, 255, 255))
                screen.blit(text_surface, (100, 100))
                screen.blit(e, (100, 150))

                keys = pygame.key.get_pressed()                
                if keys[pygame.K_e]:
                    good_boi = True
                    front = False
                    game_complete = False
                    game_over = False
                    clock = pygame.time.Clock()
                    last_obstacle_time = pygame.time.get_ticks()
                    last_complete_time = pygame.time.get_ticks()

                    # Group for obstacles
                    obstacles = pygame.sprite.Group()
                    if not level == true_lvl:
                        level = true_lvl
                    else:
                        level += 1
                    player.rect.x = 250
                    player.rect.y = 520
                    player.image = pygame.image.load(dd/"images/frog.png").convert_alpha()
                    player.image = pygame.transform.scale(player.image, (75, 75))
                    special = random.randint(1, 10)
                    if special == 5:
                        print("wahh")
                        level = "car hell"
                    elif not special == 1:
                        print("ayo chill")
                        level = "waiting game"
                        waiting_time = random.randint(10000, 50000)
                    true_lvl += 1
                    
                    # self.lvl_up()
                pygame.display.update()
          
            while game_over:
                pygame.event.get()
                keys = pygame.key.get_pressed()
                oof = font.render('ya died got exploded everyone sad :c', True, (255, 255, 255))
                reset = font.render("press r to reincarnate", True, (255, 255, 255))
                screen.blit(oof, (0, 100))
                screen.blit(reset, (0, 150))
                if keys[pygame.K_r]:
                    good_boi = True
                    random_var1 = True
                    front = False
                    game_over = False
                    clock = pygame.time.Clock()
                    last_obstacle_time = pygame.time.get_ticks()
                    last_complete_time = pygame.time.get_ticks()
                    # Group for obstacles
                    
                    obstacles = pygame.sprite.Group()

                    player.rect.x = 250
                    player.rect.y = 520
                    player.image = pygame.image.load(dd/"images/frog.png").convert_alpha()
                    player.image = pygame.transform.scale(player.image, (75, 75))

                pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()

