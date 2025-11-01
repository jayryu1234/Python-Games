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
        if num == 1:
            self.rect.y -= 75
        if num == 2:
            self.rect.y += 75
        if num == 3 and not self.rect.x <= 0:
            self.rect.x -= 75
        if num == 4 and not self.rect.x >= 525:
            self.rect.x += 75
            
class laggy1000ping(sprite.Sprite):
    def __init__(self, column, dir):
        pygame.sprite.Sprite.__init__(self)
        self.dir = dir
        self.lastjump_time = 0
        self.image = pygame.image.load(dd/"images/frog.png").convert_alpha()


        self.image = pygame.transform.scale(self.image, (75, 75))
        self.mask = pygame.mask.from_surface(self.image)
        if self.dir == "left":
            self.angle = -90
        else:
            self.angle = 90
        self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        if dir == "left":
            self.rect.x = 0
        if dir == "right":
            self.rect.x = 525
        self.rect.y =520-  column *75
        self.rect.center = self.rect.center
    def update(self):
        # if pygame.time.get_ticks() - self.deathclock >= 1000 and not self.deathclock == 0:
        #     self.kill()
        # elif pygame.time.get_ticks() - self.starting_time > 1000:
        #     self.image = pygame.image.load(dd/"images/explosion1.gif")
        #     self.deathclock = pygame.time.get_ticks()

        if self.dir == "left" and pygame.time.get_ticks() - self.lastjump_time >= 500:
            if self.rect.right > 525:
                 self.kill()
            self.rect.x += 100
            self.lastjump_time = pygame.time.get_ticks()
        elif self.dir == "right" and pygame.time.get_ticks() - self.lastjump_time >= 300:
            if self.rect.left < 0:
                self.kill()
            self.rect.x -= 100
            self.lastjump_time = pygame.time.get_ticks()
class ZZZ(sprite.Sprite):
    def __init__(self, column, dir, weight):
        pygame.sprite.Sprite.__init__(self)
        self.deathclock = 0
        self.starting_time = pygame.time.get_ticks()
        self.pounds = weight
        self.dir = dir
        if dir == "left":
            self.image = pygame.image.load(dd/"images/carRight.png").convert_alpha()
        if dir == "right":
            self.image = pygame.image.load(dd/"images/carLeft.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (weight + 50, weight + 50))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        if dir == "left":
            self.rect.x = 0
        if dir == "right":
            self.rect.x = 525
        self.rect.y =520-  column *75
        self.rect.center = self.rect.center
    def update(self):
        if pygame.time.get_ticks() - self.deathclock >= 1000 and not self.deathclock == 0:
            self.kill()
        elif pygame.time.get_ticks() - self.starting_time > 1000:
            self.image = pygame.image.load(dd/"images/explosion1.gif")
            self.deathclock = pygame.time.get_ticks()

        elif self.dir == "left":
            if self.rect.right > 525:
                 self.kill()

            self.rect.x += 5 - self.pounds / 30
        elif self.dir == "right":
            if self.rect.left < 0:
                self.kill()
            self.rect.x -= 5 - self.pounds / 30
class Bomb(sprite.Sprite):
    def __init__(self, column, dir, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.dir = dir
        self.image = pygame.image.load(dd/"images/explosion1.gif").convert_alpha()

        self.image = pygame.transform.scale(self.image, (50, 50))
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

            self.rect.x += 5 + self.speed
        if self.dir == "right":
            if self.rect.left < 0:
                self.kill()
            self.rect.x -= 5 + self.speed 
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

    def add_obstacle(self, obstacles, type):
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
            if type == 1:
                obstacle = Car(dir = dir, column = column)
            elif type == 2:
                obstacle = Bomb(dir = dir, column = column, speed = random.randint(3, 8))
            elif type == "BIG":
                obstacle = ZZZ(dir = dir, column = column, weight = random.randint(90, 150))
            elif type == "LAG":
                obstacle = laggy1000ping(dir = dir, column = column)
            obstacles.add(obstacle)
            return 1
    
    def mainloop(self):
        timebomb = False
        bdo = False
        bdo_enabled = False
        detonation_check =True
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
        null = False
        bad_boi = False
        level = 1
        true_lvl = 1
        good_boi = True
        game_complete = False
        game_over = False
        hepressed = False
        aa= 0
        b= 0
        c= 0
        while running:
            while not game_over and not game_complete and not null:


                if level == "car hell":
                        
                        if pygame.time.get_ticks() - last_obstacle_time > 1000:

                            for i in range(4):
                                    self.obstacle_count += Game.add_obstacle(self, obstacles, 1)
                                    last_obstacle_time = pygame.time.get_ticks()
                elif level == "BIG MACS":
                    if pygame.time.get_ticks() - last_obstacle_time > 800:
                                last_obstacle_time = pygame.time.get_ticks()
                                self.obstacle_count += Game.add_obstacle(self, obstacles, "BIG")
                                if random.randint(1, 4) == 2:
                                    last_obstacle_time = pygame.time.get_ticks()
                                    self.obstacle_count += Game.add_obstacle(self, obstacles, 2)
                elif level == "waiting game":
                        if good_boi == True:
                            if pygame.time.get_ticks() - last_obstacle_time > 1200:
                                last_obstacle_time = pygame.time.get_ticks()
                                self.obstacle_count += Game.add_obstacle(self, obstacles, 1)
                        else:
                            for i in range(10):
                                self.obstacle_count += Game.add_obstacle(self, obstacles, 2)
                elif int(level) <= -1:
                    if pygame.time.get_ticks() - last_obstacle_time > 600:
                        self.obstacle_count += Game.add_obstacle(self, obstacles, "LAG")
                        last_obstacle_time = pygame.time.get_ticks()
                elif level >= 5:           
                    if pygame.time.get_ticks() - last_obstacle_time > 350:
                                last_obstacle_time = pygame.time.get_ticks()
                                self.obstacle_count += Game.add_obstacle(self, obstacles, 1)
                                if random.randint(1, 7) == 2:
                                    last_obstacle_time = pygame.time.get_ticks()
                                    self.obstacle_count += Game.add_obstacle(self, obstacles, 2)
                elif pygame.time.get_ticks() - last_obstacle_time > 400 - level*20:
                            last_obstacle_time = pygame.time.get_ticks()
                            self.obstacle_count += Game.add_obstacle(self, obstacles, 1)
                

                obstacles.update()
                if player.rect.y >= 520:
                    if front == True:
                        game_complete = True
                        pygame.display.update()
                    if player.rect.y >= 670:
                        password = input("password?")
                        if password == "negative 0":
                            print("""i = invincibility
                                  n = negative world
                                  t = teleport to level
                                  bdo = back delay off (op, and press q if you want to toggle (after u enable bdo))
                                  a = ascension
                                  n = nuclear bomb""")
                            dev_console = input("what console do you want to use?")
                            if dev_console == "n":
                                random1 = input("time or detonation? (time = t detonation = d)")
                                if random1 == "t":
                                    random2 = input("level or ticks? (lvl = l, ticks = t)")
                                    if random2 == "l":
                                        timebomb_lvl = input("what level >:D")
                                        timebomb = True
                                        
                                    if random2 == "t":
                                        timebombticks = input("how many ticks till doom? >:)))))")
                                        timebomb = True
                                        bombcreattime = pygame.time.get_ticks()

                                if random1 == "d":
                                    print("kkk, press b to cause some TROLLINNN")
                                    detonation_check =True

                            if dev_console == "t":
                                tp_level = input("what lvl do ya wana teleport 2")

                                try:
                                    level = int(tp_level) - 1
                                    if int(level) == level:
                                        true_lvl = level
                                except ValueError:
                                    level = tp_level
                                game_over = True
                            elif dev_console == "bdo":
                                bdo_enabled = True
                                game_over = True
                        else:
                            print("WRONGGGGGG GETTTOUTTTT")
                            while True:
                                self.add_obstacle(obstacles, type= "BIG")

                        game_complete = True
                        pygame.display.update()
                if player.rect.y <= -75:
                    if not player.rect.y <= -200:
                        font = pygame.font.SysFont("Arial", 30)

                        if level == "waiting game" and pygame.time.get_ticks() - last_complete_time < waiting_time:
                            text_surface = font.render("bad boiii", True, (255, 255, 255))
                            good_boi = False
                        else:
                            text_surface = font.render("go backk", True, (255, 255, 255))
                        
                        front = True
                        screen.blit(text_surface, (100, 100))
                        pygame.display.update()
                    elif player.rect.y <= -200 and player.rect.y >= -1000:
                        text_surface = font.render("bro whatya think yar doin", True, (255, 255, 255))
                        screen.blit(text_surface, (100, 100))
                        pygame.display.update()

                    elif player.rect.y <= 1000 and player.rect.y >= -2500:
                        text_surface = font.render("im warning you", True, (255, 255, 255))
                        screen.blit(text_surface, (100, 100))
                        pygame.display.update()
                    else:
                        level = -2
                        true_lvl = level
                        game_complete = True

                for event in pygame.event.get():
                    current_time = pygame.time.get_ticks()
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b and detonation_check == True:
                            null = True
                        if event.key == pygame.K_q and bdo_enabled == True:
                            if bdo == True:
                                bdo = False
                            if bdo == False:
                                bdo = True
                        if event.key == pygame.K_w and not ismovin:
                            last_hold_time = current_time
                            player_group.update(1)
                            ismovin = True
                            hepressed = True
                        elif event.key == pygame.K_s:
                            if bdo == True:
                                last_hold_time = current_time
                                player_group.update(2)
                                hepressed = True
                                ismovin = True
                            else:
                                if current_time - last_hold_time >= 500:
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
                if level == "BIG MACS":
                    prompt = "warning warning"
                # if level == 7:
                #     prompt = "new york style 💀"
                if level == "waiting game":
                    prompt = 'huh'
                try: 
                    if level >= 6:
                        prompt = "way 2 hard"
                except TypeError:
                    pass
                if bad_boi == True:
                    prompt = 'BAD BOI'
                car_cd = font.render(f"cars trafficking level: {prompt}", True, (255, 255, 255))
                if level == 6:
                    prompt2 = "???"
                if level == "BIG MACS":
                    prompt2 = "BIG PEOPLE INCOMIN"
                if level == "waiting game":


                    if not bad_boi == True:
                        prompt2 = "this ez level for break time"
                    else:
                        prompt2 = "GRR GRR PATAPIM"
                    
                else:
                    prompt2 = level
                level_text = font.render(f'Level: {prompt2}', True, (255, 255, 255))
                waiting_text = font.render(f'{waiting_time - (pygame.time.get_ticks() - last_complete_time)}', True, (255, 255, 255))
                if level == "waiting game" or level == "car hell" or level == "BIG MACS" or timebomb == True:
                    aa += 1
                    b += 2
                    c += 3
                    if aa >= 255:
                        aa = 0
                    if b >= 255:
                        b = 0
                    if c >= 255:
                        c= 0

                    if not level == "BIG MACS" or not timebomb == True:
                        special_level = font.render(f'SPECIAL LEVEL!!!', True, (aa, b, c))
                    if level == 'BIG MACS':

                        special_level = font.render(f'TS IS INFLATION', True, (aa, b, c))
                    if timebomb == True:
                        timebombtickstext = font.render(f'time till doom! {int(timebombticks)- (pygame.time.get_ticks() - bombcreattime)}', True, (aa, b, c))
                        
                screen.blit(BACKGROUND, (0, 0))
                screen.blit(level_text, (25, 25))
                screen.blit(car_cd, (25, 65))
                try:
                    if level == "waiting game":
                        screen.blit(waiting_text, (25, 135))
                except UnboundLocalError:
                    pass
                try:
                    if level == "car hell" or level == "waiting game" or level == "BIG MACS" and not timebomb == True:
                        screen.blit(special_level, (25, 100))
                except UnboundLocalError:
                    pass
                try:
                    screen.blit(timebombtickstext, (25, 100))
                    if int(timebombticks) - (pygame.time.get_ticks() -bombcreattime) <= 0:
                        null = True
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
                    if not level <= -1:

                        if special == 6:
                            level = "BIG MACS"
                        elif special == 5:
                            print("wahh")
                            level = "car hell"
                        elif special == 1:
                            print("ayo chill")
                            level = "waiting game"
                            waiting_time = random.randint(10000, 50000)
                    true_lvl += 1
                    
                    # self.lvl_up()
                pygame.display.update()
            while null:
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont("Arial", 30)
                pygame.event.get()
                keys = pygame.key.get_pressed()
                riddle_font = pygame.font.SysFont("Display", 20)
                oof = font.render('you just got jebaited', True, (255, 255, 255))
                reset = font.render("press t for a chance to come back.", True, (255, 255, 255))
                screen.blit(oof, (0, 100))
                screen.blit(reset, (0, 150))
                if keys[pygame.K_t]:
                    lol = font.render('now press f', True, (255, 255, 255))
                    screen.blit(lol, (0, 190))
                if keys[pygame.K_f]:
                    more = font.render('now press z', True, (255, 255, 255))
                    screen.blit(more, (0, 230))
                if keys[pygame.K_z]:
                    heh = font.render('good boiii XD, now press r to go back', True, (255, 255, 255))
                    screen.blit(heh, (0, 270))
                if keys[pygame.K_r]:
                    jk = font.render('hah im lying of course', True, (255, 255, 255))
                    jkk = font.render("if u are bored press a", True, (255, 255, 255))
                    screen.blit(jk, (0, 310))
                    screen.blit(jkk, (0, 350))
                elif keys[pygame.K_a]:
                    lol = font.render("welp ya are bored so les play this game", True, (255, 255, 255))
                    minigame_instruction = font.render("find the next key and press it", True, (255, 255, 255))
                    screen.blit(lol, (0, 190))
                    screen.blit(minigame_instruction, (0, 230))
                    minigame_element1 = font.render("press the 24th letter from the alphabet", True, (255, 255, 255))
                    screen.blit(minigame_element1, (random.randint(0, 600), random.randint(-300, 300)))
                elif keys[pygame.K_x]:
                    minigame_element2 = riddle_font.render("""I am in the beginning of youth, the center of every eye, and the end of eternity. What am i?""", True, (255, 255, 255))
                    loser = font.render("if yar a loser and u dont know press l", True, (255, 255, 255))
                    screen.blit(minigame_element2, (0, 250))
                    screen.blit(loser, (0, 280))
                elif keys[pygame.K_l]:
                    loser = font.render("LOSER LOSER LOSER hahaha", True, (255, 255, 255))
                    more = font.render("press y LOSER", True, (255, 255, 255))
                    screen.blit(loser, (0, 230))
                    screen.blit(more, (0, 270))
                elif keys[pygame.K_y]:
                    seventhgrademath = font.render("if x^2 + 8x +16 = 0, whats abs(x)?", True, (255, 255, 255))
                    screen.blit(seventhgrademath, (0, 190))
                elif keys[pygame.K_4]:
                    final_Q = font.render("if 6 is 3 and 7 is 5, then whats 11?", True, (255, 255, 255))
                    screen.blit(final_Q, (0, 270))
                elif keys[pygame.K_7]:
                    gg = font.render("gg man, press 0 to leave, then press e", True, (255, 255, 255))
                    screen.blit(gg, (0, 190))
                elif keys[pygame.K_0]:
                    null = False
                    timebomb = False
                    game_complete = True

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