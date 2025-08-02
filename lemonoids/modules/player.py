import pygame, math
from modules.bullet import Bullet
import modules.ui as ui

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, bullet_group):
        super().__init__()
        self.original = pygame.image.load("assets/images/player.png")
        self.original = pygame.transform.scale(self.original, (60, 45))
        self.image = self.original
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_group = bullet_group
        self.rect = self.image.get_rect(center = pos)
        #self.rect = self.rect.scale_by(0.7, 0.7)
        #self.rect = self.rect.move(pos)
        self.max_health = 10
        self.health = self.max_health
        self.invincible = False
        self.invincible_timer = 0
        self.blink_timer = 0

        self.shootCounter = 0
        self.shootdelay = 3
    def move(self, dx, dy):
        speed = 5
        self.rect.x += dx * speed
        self.rect.y += dy * speed
    def update(self):
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.rect.centerx
        dy = my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        
        if self.invincible:
            self.invincible_timer -= 1
            self.blink_timer = (self.blink_timer +1) % 10
            if self.blink_timer %2:
                self.image = pygame.transform.rotate(self.original, angle)
            else:
                self.image = pygame.transform.rotate(
                    pygame.Surface(self.rect.size, pygame.SRCALPHA),
                    angle
                )
            if self.invincible_timer <= 0:
                self.invincible = False
                self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, angle)     

        self.rect = self.image.get_rect(center = self.rect.center)
        if pygame.mouse.get_pressed()[0]:
            self.shootCounter += 1
            if self.shootCounter % self.shootdelay == 0:
                Bullet.fire(self.rect.center, angle, self.bullet_group)
    def draw(self, surf):
        surf.blit(self.image, self.rect)
        ui.drawHealthBar(surf, self.rect.centerx, self.rect.y - 10, self.health, self.max_health, 1)