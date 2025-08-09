import pygame, random

class Lemon(pygame.sprite.Sprite):
    def __init__(self, pos, size = 3, img = "lemonoid.png"):
        super().__init__()
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load("lemonoids/assets/images/"+img),
            (size*70, size*50)
        )
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        
        # self.rect = self.rect.scale_by(0.7, 0.7)
        #self.rect = self.rect.move(pos)
        self.max_health = size*20
        self.health = self.max_health
        self.speed = 1
        self.set_speed(min = 1)
        
    def set_speed(self, min):
        while True:
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            if abs(self.vx) + abs(self.vy) > min:
                break

    def __init__(self, pos, size = 3, img = "lemonoid.png", imgscaleX = 70, imgscaleY = 50):
        super().__init__()
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load("lemonoids/assets/images/"+img),
            (size*imgscaleX, size*imgscaleY)
        )
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        
        # self.rect = self.rect.scale_by(0.7, 0.7)
        #self.rect = self.rect.move(pos)
        self.max_health = size*20
        self.health = self.max_health
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

    def split(self):
        fragments = []
        numsFrag = 0
        if self.size > 2:
            numsFrag=2
        elif self.size == 2:
            numsFrag=3
        for _ in range(numsFrag):
            frag = type(self)(self.rect.center, self.size - 1)
            fragments.append(frag)
        return fragments
class StrongLemon(Lemon):
    def __init__(self, pos, _size = 4):
        super().__init__(pos, size=_size, img = "Strong_Lemon.png", imgscaleX=70, imgscaleY= 50)
        self.max_health = self.size*20
        self.health = self.max_health
        self.mask = pygame.mask.from_surface(self.image)

class StrongerLemon(Lemon):
    def __init__(self, pos, _size = 5):
        super().__init__(pos, size=_size, img = "Strong_Lemon_2.png", imgscaleX=70, imgscaleY= 50)
        self.max_health = self.size*25
        self.health = self.max_health
        self.mask = pygame.mask.from_surface(self.image)

class SpeedyLemon(Lemon):
    def __init__(self, pos,_size = 2):
        super().__init__(pos, size = _size, img = "Speedy_Lemon.png", imgscaleX=60, imgscaleY= 40)
        self.speed = 3
class BigLemon(Lemon):
    def __init__(self, pos, _size = 4):
        super().__init__(pos, size = _size, img = "lemonoid.png", imgscaleX=80, imgscaleY= 59)
        self.max_health = self.size * 10
        self.speed = 0.85
class SpeedierLemon(Lemon):
    def __init__(self, pos, _size = 2):
        super().__init__(pos, size = _size, img = "SpeedyLemon_2.png", imgscaleX=54, imgscaleY= 43)
        self.max_health= self.size*30
        self.speed = 3.5
class SpeedyPlus(Lemon):
    def __init__(self, pos, _size = 3):
        super().__init__(pos, size = _size, img = "Speedy_PLUS.png", imgscaleX= 45, imgscaleY= 35)
        self.max_health= self.size*30
        self.speed = 2.3  

#special lemons!

class HealerLemon(Lemon):
    pass
class TankLemon(Lemon):
    pass