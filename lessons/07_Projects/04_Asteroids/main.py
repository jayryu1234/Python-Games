import pygame, random
from pygame.locals import *
from pygame import sprite
from pathlib import Path
dd = Path(__file__).parent
screen = pygame.display.set_mode((600, 600))
#fill screen
import math

class Asteroids(sprite.Sprite):
    def __init__(self, pos, img, size):
        super().__init__()
        self.img = img
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load(dd/f"images/{img}"),
            (self.size*35, self.size*25)
        )
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 8
        # self.rect = self.rect.scale_by(0.7, 0.7)
        #self.rect = self.rect.move(pos)
        self.speed = 1
        self.set_speed(min = 1)

    def update(self):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

        screen_w, screen_h = pygame.display.get_surface().get_size()
        if self.rect.right < 0: self.rect.left = screen_w
        if self.rect.left > screen_w: self.rect.right = 0
        if self.rect.bottom < 0: self.rect.top = screen_h
        if self.rect.top > screen_h: self.rect.bottom = 0

    def set_speed(self, min):
        while True:
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            if abs(self.vx) + abs(self.vy) > min:
                break
    def split(self):
        fragments = []
        numsFrag = 0
        if self.size > 2:
            numsFrag=2
        elif self.size == 2:
            numsFrag=3
        for _ in range(numsFrag):
            frag = type(self)(self.rect.center, img = self.img, size = self.size - 1)
            fragments.append(frag)
        return fragments
    
class Player(sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original = pygame.image.load(dd/"images/ship.png").convert_alpha()
        self.original = pygame.transform.scale(self.original, (25, 25))
        self.image = self.original
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 520
        self.rect.center = self.rect.center

    def update(self):
        keys = pygame.key.get_pressed()

        # Move the square based on arrow keys
        if keys[K_w] and self.rect.y >= 150:
           self.rect.y -= 5
        if keys[K_s] and self.rect.y <= 480:
            self.rect.y += 5
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= 5
        if keys[K_a] and self.rect.x <= 10:
            self.kill()
            
        if keys[K_d] and self.rect.x < 570:
            self.rect.x += 5

        mx, my = pygame.mouse.get_pos()
        dx = mx - self.rect.centerx
        dy = my - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx))

        self.image = pygame.transform.rotate(self.original, self.angle + 270)
        self.rect = self.image.get_rect(center = self.rect.center)  

#bullets
class Bullets(sprite.Sprite):
    def __init__(self, xpos, ypos, dir, type):

        pygame.sprite.Sprite.__init__(self)
        self.dir = dir
        self.image = pygame.image.load(dd/"images/laser.png").convert_alpha()
        if type == "EMP":
            self.image = pygame.transform.scale(self.image, (350, 350))
        elif type == "TINY":
            self.image = pygame.transform.scale(self.image, (150, 150))
        self.speed = 15
        self.rect = self.image.get_rect()
        self.rect.x = xpos + 15
        if type == "EMP":
            self.rect.x = xpos - 175
        if type == "TINY":
            self.rect.x = xpos - 75
        
        self.rect.y = ypos
        self.image = pygame.transform.rotate(self.image, dir + 270)
        

    def update(self):
        screen.blit(self.image, self.rect)
        rad = math.radians(-self.dir)
        self.rect.x += self.speed * math.cos(rad)
        self.rect.y += self.speed * math.sin(rad)
        
        if self.rect.y < -50 or self.rect.y > 650:
            self.kill()

#game class
class Game(sprite.Sprite):

    def __init__(self):
        pygame.init()
        self.score = 0
        self.asteroids_count = 0

    def add_asteroid(self, obstacles):

        side = random.choice(['top','bottom','left','right'])
        w, h = pygame.display.get_surface().get_size()
        if side == 'top': pos = (random.randint(0,w),-20)
        elif side == 'bottom': pos = (random.randint(0,w),h+20)
        elif side == 'left': pos = (-20,random.randint(0,h))
        elif side == 'right': pos = (w+20,random.randint(0,h))

        randomnumber = random.randint(1, 4)
        if randomnumber == 1 or randomnumber == 4:
            img = "spaceMeteors_001.png"
        elif randomnumber == 2:
            img = "asteroid1.png"
        else:
            img = "alien1.gif"
        asteroids = Asteroids(pos = pos, img = img, size = 3)
        obstacles.add(asteroids)
        return 1
    
    def mainloop(self):
        aa = 0
        b = 0
        c = 0
        mouse_held_down = False
        last_obstacle_time = pygame.time.get_ticks()
        last_shot_time = 0
        self.keys = pygame.key.get_pressed()
        clock = pygame.time.Clock()
        last_reroll_time = 0
        enemy_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        specials_group = pygame.sprite.Group()
        last_EMP_time = 0
        player = Player()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        sprite_group = pygame.sprite.Group()
        EMP_FLURRY = False
        RUSH_HOUR = False
        sprite_group.add(player)

        while True:
            if self.score <= 15:
                bullet_refill = 200
            elif self.score < 75:
                bullet_refill = 150
            elif self.score < 150:
                bullet_refill = 100
            elif self.score < 250:
                bullet_refill = 75
            self.keys = pygame.key.get_pressed()

            screen.fill((0, 0, 0))
            #reroll for perks :P
            if pygame.time.get_ticks() - last_reroll_time >= 5000:

                last_reroll_time = pygame.time.get_ticks()
                chance = random.randint(1, 5)
                if chance == 1:
                    EMP_FLURRY = True
                    flurry_time = pygame.time.get_ticks()
                    
                    print("O YA")
                elif not chance == 2:
                    RUSH_HOUR = True
                
                reroll_text = font.render("reroll", True, (255, 255, 0))
                screen.blit(reroll_text, (250, 300))
            for event in pygame.event.get():
                if self.keys[K_SPACE]:
                    #EMP :P
                    if not EMP_FLURRY:
                        current_time = pygame.time.get_ticks()
                        if current_time - last_EMP_time >= 10000:
                            last_EMP_time = current_time
                            EMP= Bullets(
                                player.rect.x,
                                player.rect.y,
                                player.angle,
                                "EMP"
                            )
                            specials_group.add(EMP)
                            sprite_group.add(EMP)
                    else:
                        current_time = pygame.time.get_ticks()
                        if current_time - last_EMP_time >= 100:
                            last_EMP_time = current_time
                            EMP= Bullets(
                                player.rect.x,
                                player.rect.y,
                                player.angle,
                                "TINY"
                            )
                            specials_group.add(EMP)
                            sprite_group.add(EMP)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #checking if its down
                    if event.button == 1:  # Left mouse button
                        mouse_held_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_held_down = False
    
                if event.type == QUIT:
                    pygame.quit()

            #check if emp flurry is up
            if EMP_FLURRY:
                if pygame.time.get_ticks() - flurry_time >= 5000:
                    EMP_FLURRY = False
            # Check if enough time has passed to fire another shot
            if mouse_held_down:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= bullet_refill:
                    last_shot_time = current_time
                    bullets = Bullets(
                    player.rect.x,
                    player.rect.y,
                    player.angle,
                    "normal"
                )      
                
                    bullet_group.add(bullets)
                    sprite_group.add(bullets)
            if RUSH_HOUR:
                for i in range(random.randint(5, 10)):
                    if pygame.time.get_ticks() - last_obstacle_time > 300 - pygame.time.get_ticks()//50 + self.score:
                        last_obstacle_time = pygame.time.get_ticks()
                        self.asteroids_count += Game.add_asteroid(self, enemy_group)
                RUSH_HOUR = False
            if pygame.time.get_ticks() - last_obstacle_time > 800 - pygame.time.get_ticks()//50 + self.score:
                        last_obstacle_time = pygame.time.get_ticks()
                        self.asteroids_count += Game.add_asteroid(self, enemy_group)
                
            
        #update (enemy + player)
            
            enemy_group.update()

            enemy_group.draw(screen)
            
            sprite_group.update()
            sprite_group.draw(screen)
            font = pygame.font.SysFont("Arial", 30)
            if EMP_FLURRY:
                emp_left = 100 - (pygame.time.get_ticks() - last_EMP_time)
            else:
                emp_left = 10000 - (pygame.time.get_ticks() - last_EMP_time)
            if emp_left <= 0:
                emp_left = 0
            if EMP_FLURRY:
                aa += 1
                b += 2
                c += 3
                if aa >= 255:
                    aa = 0
                if b >= 255:
                    b = 0
                if c >= 255:
                    c= 0
                emp_time = font.render(f"EMP FLURRY GOGOGO {5000 - pygame.time.get_ticks() + flurry_time}", True, (aa, b, c))
            elif RUSH_HOUR:
                emp_time = font.render(f"RUSH HOUR", True, (255, 255, 255))
            else:
                emp_time = font.render(f"EMP :P {emp_left}", True, (255, 255, 255))
            reroll_time = 5000 - pygame.time.get_ticks() + last_reroll_time
            if RUSH_HOUR:
                reroll = font.render("KILL THEM ALLL")
            elif EMP_FLURRY:
                reroll = font.render("I CaNT StOp WInnInG", True, (255, 0, 0))
            else:
                reroll = font.render(f"reroll: {reroll_time}", True, (255, 0, 255))
            screen.blit(reroll, (10, 40))
            screen.blit(emp_time, (10, 100))
            score_text = font.render(f"Score: {self.score}", True, (255,255,0))
            screen.blit(score_text, (10, 70))
            pygame.display.update()
            clock.tick(40)
            hits = pygame.sprite.groupcollide(enemy_group, bullet_group ,False,True)
            hits2 = pygame.sprite.groupcollide(enemy_group, specials_group, True, False)
            for meteor, bs in hits.items():
                meteor.health -= len(bs) * 8 # player damage

                if meteor.health <= 0:
                    for frag in meteor.split():
                        self.score += 1
                        enemy_group.add(frag)

                    meteor.kill()
                else:
                    pass
            for meteor, bs in hits2.items():
                self.score += 0.5
                meteor.kill()
            self.score = math.ceil(self.score)
            # pygame.sprite.groupcollide(bullet_group, enemy_group, True, True, pygame.sprite.collide_mask)
            
            pygame.sprite.groupcollide(player_group, enemy_group, True, True, pygame.sprite.collide_mask)
                  


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()