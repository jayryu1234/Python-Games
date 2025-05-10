import pygame, random
from pygame.locals import *
from pathlib import Path

#VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15
BLACK = (0, 0, 0)
GROUND_WIDTH = 2 * SCREEN_HEIGHT
GROUND_HEIGHT= 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150
score = 0

dd = Path(__file__).parent

pygame.mixer.init()

wing = dd/'assets/audio/wing.wav'
hit = dd/'assets/audio/hit.wav'
class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dd/"assets/sprites/base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH*3, SCREEN_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_offscreenprob(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()

class Bird(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.images =  [pygame.image.load(dd/"assets/sprites/redbird-downflap.png").convert_alpha(),
                        pygame.image.load(dd/"assets/sprites/redbird-midflap.png").convert_alpha(),
                        pygame.image.load(dd/"assets/sprites/redbird-upflap.png").convert_alpha()]
        
        self.movingspeed = SPEED

        self.currentimage = 0
        self.rightnowimage = pygame.image.load(dd/"assets/sprites/redbird-downflap.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.rightnowimage)

        self.rect = self.rightnowimage.get_rect()
        self.rect[0] = SCREEN_WIDTH /6
        self.rect[1] = 300
    
    def update(self):
        self.currentimage = (self.currentimage+1)%3
        self.image = self.images[self.currentimage]
        self.movingspeed += 2.5

        self.rect[1] += self.movingspeed

    def bump(self):
        self.movingspeed = -SPEED
    
    def rotate(self):
        self.currentimage = (self.currentimage+1)%3
        self.image = self.images[self.currentimage]

        

    
class Pipe(pygame.sprite.Sprite):
    def __init__(self, flipped, xposition, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(dd/'assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xposition

        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ypos)
        else:
            #soooo this is basically y = screen height - the y position variable or something
            self.rect[1] = SCREEN_HEIGHT - ypos
    
    def update(self):
        if self.rect.x >= 65 and self.rect.x <= 66:
            global score
            score += 0.5

        self.rect[0] -= GAME_SPEED

def get_random_pipes(xposition):
    size = random.randint(100, 300)
    pipe = Pipe(False, xposition, size)
    pipe_flipped = Pipe(True, xposition, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_flipped


pygame.init()

    
    
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


BACKGROUND = pygame.image.load(dd / 'assets/sprites/background-night.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load(dd/ 'assets/sprites/message.png').convert_alpha()

def main():
    
    global score
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()

    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()

    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i +800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    
    clock = pygame.time.Clock()

    start = True

    while start:
        
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
                    start = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (120, 150))

        if is_offscreenprob(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        bird.rotate()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

    while True:
        clock.tick(15)

        screen.blit(BACKGROUND, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
        if is_offscreenprob(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)
        if is_offscreenprob(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])

                pipes = get_random_pipes(SCREEN_WIDTH * 2)

                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])
            
        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)
        pipe_group.draw(screen)

        font = pygame.font.SysFont(None, 36)
        end = font.render(f"SCORE: {int(score)}", True, BLACK)
        screen.blit(end,(30, 30))
        pygame.display.update()

        if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask):
             
            break

            

while True:
    main()

