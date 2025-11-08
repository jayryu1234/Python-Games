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
        
        self.health = 0
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
        # self.original = pygame.transform.scale(self.image, (75, 75))
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

class Bullets(sprite.Sprite):
    def __init__(self, xpos, ypos, dir):

        pygame.sprite.Sprite.__init__(self)
        self.dir = dir
        self.image = pygame.image.load(dd/"images/laser.png").convert_alpha()
        self.speed = 20
        self.rect = self.image.get_rect(topleft = (xpos + 20, ypos)) 

    def update(self):
        screen.blit(self.image, self.rect)
        rad = math.radians(-self.dir)
        self.rect.x += self.speed * math.cos(rad)
        self.rect.y += self.speed * math.sin(rad)
        
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()

class Game(sprite.Sprite):

    def __init__(self):
        pygame.init()
        self.asteroids_count = 0

    def add_asteroid(self, obstacles):

        side = random.choice(['top','bottom','left','right'])
        w, h = pygame.display.get_surface().get_size()
        if side == 'top': pos = (random.randint(0,w),-20)
        elif side == 'bottom': pos = (random.randint(0,w),h+20)
        elif side == 'left': pos = (-20,random.randint(0,h))
        elif side == 'right': pos = (w+20,random.randint(0,h))

        randomnumber = random.randint(1, 5)
        if randomnumber == 1 or randomnumber == 4:
            img = "spaceMeteors_001.png"
        elif randomnumber == 2:
            img = "asteroid1.png"
        elif randomnumber == 3:
            img = "asteroid2.png"
        else:
            img = "alien1.gif"
        asteroids = Asteroids(pos = pos, img = img, size = 3)
        obstacles.add(asteroids)
        return 1
    
    def mainloop(self):
        last_obstacle_time = pygame.time.get_ticks()
        last_shot_time = 0
        self.keys = pygame.key.get_pressed()
        clock = pygame.time.Clock()

        enemy_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
  
        player = Player()
        player_group = pygame.sprite.Group()
        player_group.add(player)
        sprite_group = pygame.sprite.Group()

        sprite_group.add(player)

        while True:
            self.keys = pygame.key.get_pressed()

            screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if self.keys[K_SPACE]:

                        # Check if enough time has passed to fire another shot
                        current_time = pygame.time.get_ticks()
                        if current_time - last_shot_time >= 100:
                            last_shot_time = current_time
                            bullets = Bullets(
                            player.rect.x,
                            player.rect.y,
                            player.angle
                        )      
                        
                            bullet_group.add(bullets)
                            sprite_group.add(bullets)
                if event.type == QUIT:
                    pygame.quit()

            if pygame.time.get_ticks() - last_obstacle_time > 500:
                        last_obstacle_time = pygame.time.get_ticks()
                        self.asteroids_count += Game.add_asteroid(self, enemy_group)
                
            
        #update (enemy + player)
            
            enemy_group.update()

            enemy_group.draw(screen)
            
            sprite_group.update()
            sprite_group.draw(screen)
            pygame.display.update()
            pygame.display.update()
            clock.tick(40)
            hits = pygame.sprite.groupcollide(enemy_group, bullet_group ,False,True)
            for meteor, bs in hits.items():
                meteor.health -= len(bs) * 8 # player damage
                
                if meteor.health <= 0:
                    for frag in meteor.split():
                        enemy_group.add(frag)

                    meteor.kill()
                else:
                    pass
            # pygame.sprite.groupcollide(bullet_group, enemy_group, True, True, pygame.sprite.collide_mask)
            
            pygame.sprite.groupcollide(player_group, enemy_group, True, True, pygame.sprite.collide_mask)
                  


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.mainloop()