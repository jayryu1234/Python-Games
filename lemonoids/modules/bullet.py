import pygame
import math
import modules.audio as sfx
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.original = pygame.image.load("lemonoids/assets/images/laser.png")
        self.original = pygame.transform.scale(self.original, (10, 40))
        self.image = pygame.transform.rotate(self.original, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        self.speed = 10
    def update(self):
        rad = math.radians(-self._angle)
        self.rect.x += self.speed * math.cos(rad)
        self.rect.y += self.speed * math.sin(rad)
    @classmethod
    def fire(cls, pos, angle, group):
        
        bullet = cls(pos, angle)
        bullet._angle = angle
        group.add(bullet)
        sfx.play_sfx(sound= "shoot",channel_id=5)