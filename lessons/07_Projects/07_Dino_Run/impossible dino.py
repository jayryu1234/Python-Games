"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path
dd = Path(__file__).parent
import time
jumpCount = 10
# Initialize Pygame
pygame.init()
images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
pygame.display.set_caption("Dino Jump")

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# FPS
FPS = 60

# Player attributes
PLAYER_SIZE = 50

player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 20
obstacle_speed = 10

# Font
font = pygame.font.SysFont(None, 36)

# Define an obstacle class print
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.pto = random.randint(1, 10)
        self.pto_height = random.randint(1, 3)
        self.pto_speed = random.randint(1, 3)
        self.player = player
        self.temp = self.player.score
        self.cactus_height = random.randint(1, 3)
        if self.pto == 1 and self.temp >= 10:
            self.images =[pygame.transform.scale(pygame.image.load(dd/"images/ptero_0.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE)),
                        pygame.transform.scale(pygame.image.load(dd/"images/ptero_1.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))]
            print('PTO' + str(self.pto_height) + str(self.pto_speed))
        elif self.cactus_height == 1:
            self.image = pygame.transform.scale(pygame.image.load(dd/"images/cactus_9.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
        elif self.cactus_height == 2:
            self.image = pygame.transform.scale(pygame.image.load(dd/"images/cactus_9.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE-10))
        elif self.cactus_height == 3:
            self.image = pygame.transform.scale(pygame.image.load(dd/"images/cactus_9.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE+5))
        
        self.currentimage = 1
        if self.pto == 1 and self.temp >= 10:
            self.image = self.images[0]
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        if self.pto_height == 1 and self.pto == 1 and self.temp >= 10:
            self.rect.y = HEIGHT - PLAYER_SIZE
        elif self.pto_height == 2 and self.pto == 1 and self.temp >= 10:
            self.rect.y = HEIGHT - PLAYER_SIZE - 20
        elif self.pto_height == 3 and self.pto == 1 and self.temp >= 10:
            self.rect.y = HEIGHT - 2*PLAYER_SIZE
        elif self.cactus_height == 1:
            self.rect.y = HEIGHT - PLAYER_SIZE
        elif self.cactus_height == 2:
            self.rect.y = HEIGHT - PLAYER_SIZE+10
        elif self.cactus_height == 3:
            self.rect.y = HEIGHT - PLAYER_SIZE -5

        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
        self.type = ""
        exploding_number = random.randint(1, 50)
        slow_guy = random.randint(1, 50)
        random_input = random.randint(1, 1000)
        # if self.temp >= 23:
        #     random_input = random.randint(1, 1)
        if random_input == 1:
            self.type = "trololol"
        elif exploding_number == 2:
            self.type = "explode"
        
        elif slow_guy == 3:
            self.type = "slow"
        else: 
            self.type = "normal"

    def update(self):
        if self.pto == 1 and self.temp >= 10:
            self.currentimage = (self.currentimage+0.1)%2
            self.image = self.images[int(self.currentimage//1)]
        if self.pto_speed == 2 and self.pto == 1 and self.temp >= 10:
            self.rect.x -= 1.05 * obstacle_speed
        if self.pto_speed == 3 and self.pto == 1 and self.temp >= 10:
            self.rect.x -= 0.9 * obstacle_speed
        if self.type == "explode":
            self.rect.x -= 1.3 * obstacle_speed
        if self.type == "slow":
            self.rect.x -= obstacle_speed * 0.8
        else:
            self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()
        if self.type == "explode":
                self.image = self.explosion
                self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
                self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.x == 50:
            self.player.score += 1
        if self.type == "trololol":
            self.rect.y = self.player.rect.y

    # def explode(self):
    #     """Replace the image with an explosition image."""
        
    #     # Load the explosion image
    #     self.image = self.explosion
    #     self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    #     self.rect = self.image.get_rect(center=self.rect.center)


# Define a player class

class  Settings():
    jump_count = 13

settings = Settings()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.last_jump = 0
        
        self.images = [pygame.transform.scale(pygame.image.load(dd/"images/dino_2.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE)),
                       pygame.transform.scale(pygame.image.load(dd/"images/dino_3.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))]
        self.jump_image = pygame.transform.scale(pygame.image.load(dd/"images/dino_0.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
        
        self.jump_count = 0
        self.jump_counter = 0
        self.currentimage = 1
        self.image = self.images[0]
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_SIZE
        self.speed = player_speed
        self.is_jumping = False
        self.score = 0

    def rotate(self):
        self.currentimage = (self.currentimage+0.1)%2
        self.image = self.images[int(self.currentimage//1)]

    def update(self):
        if not self.is_jumping:
            self.currentimage = (self.currentimage+0.1)%2
            self.image = self.images[int(self.currentimage//1)]
        else:
            self.image = self.jump_image
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping and not self.jump_counter >= 3:
        # Jumping means that the player is going up. The top of the 
        # screen is y=0, and the bottom is y=SCREEN_HEIGHT. So, to go up, 
        # we need to have a negative y velocity

            self.last_jump = pygame.time.get_ticks()
            if self.jump_counter == 1:
                self.speed = -10
            elif self.jump_counter == 0:
                self.speed = -13
            elif self.jump_counter == 2:
                self.speed = -7
            self.is_jumping = True
            self.jump_count += 1
            self.jump_counter += 1

        self.speed += 1
        self.rect.y += self.speed

        if self.rect.top < 0 :
            self.rect.top = 0
            self.speed = 0
        
        self.is_jumping = (pygame.time.get_ticks() - self.last_jump) < 200
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed = 0
            self.is_jumping = False
            self.jump_counter = 0

# Create a player object


# Add obstacles periodically
class Game():
    def __init__(self):
        pygame.init()
        self.scene = 0
        self.obstacle_count = 0


    def add_obstacle(self, obstacles, player):
        # random.random() returns a random float between 0 and 1, so a value
        # of 0.25 means that there is a 25% chance of adding an obstacle. Since
        # add_obstacle() is called every 100ms, this means that on average, an
        # obstacle will be added every 400ms.
        # The combination of the randomness and the time allows for random
        # obstacles, but not too close together. 
        
        if random.random() < 0.5:
            obstacle = Obstacle(player)
            obstacles.add(obstacle)
            return 1
        return 0


    # Main game loop
    def game_loop(self):
        global clock
        clock = pygame.time.Clock()

        player = Player()
        player_group = pygame.sprite.GroupSingle(player)
        
        game_over = False
        last_obstacle_time = pygame.time.get_ticks()

        # Group for obstacles
        obstacles = pygame.sprite.Group()
    
        while True:
            if not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # Update player
                player_group.update()

                # Add obstacles and update

              
                if pygame.time.get_ticks() - last_obstacle_time > 500:
                        last_obstacle_time = pygame.time.get_ticks()
                        self.obstacle_count += Game.add_obstacle(self, obstacles, player)
                
                obstacles.update()

                # Check for collisions
                collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
                if collider:
                     # .append(self.obsta_type)
                     game_over = True
                
                # Draw everything
                screen.fill(WHITE)
                player_group.draw(screen)
                # pygame.draw.rect(screen, BLUE, player)
                obstacles.draw(screen)

                # Display obstacle count
                score_text = font.render(f"Score: {player.score}", True, BLACK)
                screen.blit(score_text, (10, 10))

                pygame.display.update()
                clock.tick(FPS)

        # Game over screen
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                keys = pygame.key.get_pressed()
                screen.fill(WHITE)
                # if obstacle.type == "explode":
                #     end = font.render(f"LOL U DIED TO THE EASIEST TROLL ENEMY", True, BLACK)
                # elif obstacle.type == "trololol":
                #     end = font.render(f"WELP, UR LUCKY U EVEN GOT THE ENEMY XD", True, BLACK)

                end = font.render(f"OOF U DIED UR SCORE IS: {player.score}", True, BLACK)
                screen.blit(end,(30, 30))
                instructions = font.render("press space key to try again", True, BLACK)
                screen.blit(instructions, (100, 100))
                if keys[pygame.K_SPACE]:
                    game_over = False
                    clock = pygame.time.Clock()
                    last_obstacle_time = pygame.time.get_ticks()
                    player.score = 0
                    # Group for obstacles
                    obstacles = pygame.sprite.Group()

                pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.game_loop()