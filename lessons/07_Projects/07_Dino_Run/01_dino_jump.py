"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path
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
PLAYER_SIZE = 25

player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 20
obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)

# Define an obstacle class print
print("collin is bad at this game unless he gets a 25 score or higher which he never will")
print("if jay gets a 25 before collin then collin gets a knee surgery tomorow")
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - OBSTACLE_HEIGHT - 10
        self.player = player
        self.temp = self.player.score
        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
        self.type = ""
        exploding_number = random.randint(1, 10)

        slow_guy = random.randint(1, 10)
        random_input = random.randint(1, 150)
        if self.temp >= 23:
            random_input = random.randint(1, 1)
        if random_input == 1:
            self.type = "trololol"
        elif exploding_number == 3:
            self.type = "explode"
        
        elif slow_guy == 3:
            self.type = "slow"
        else: 
            self.type = "normal"
        
    def update(self):
        if self.type == "explode":
            self.rect.x -= 1.8 * obstacle_speed
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
        if self.rect.x == player.rect.x:
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
        super().__init__()
        self.image = pygame.image.load(images_dir / "explosion1.gif")

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_SIZE - 10
        self.speed = player_speed
        self.is_jumping = True
        self.score = 0
        self.type = ""
        self.jump_count = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping == True:
        # Jumping means that the player is going up. The top of the 
        # screen is y=0, and the bottom is y=SCREEN_HEIGHT. So, to go up,
        # we need to have a negative y velocity
            self.speed = -12
            self.is_jumping = True
            self.jump_count += 1
        # if not self.rect.top < 0:
        #     print("w")
        #     if keys[pygame.K_SPACE] and not self.jump_count >= 2:
        #         self.speed = -7
        #         self.jump_count += 1
        #         print("w")
        #         # self.is_jumping = False
        

    # Update player position. Gravity is always pulling the player down,
    # which is the positive y direction, so we add GRAVITY to the y velocity
    # to make the player go up more slowly. Eventually, the player will have
    # a positive y velocity, and gravity will pull the player down.
        self.speed += 1
        self.rect.y += self.speed

        if self.rect.top < 0 :
            self.rect.top = 0
            self.speed = 0
            self.jump_count = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed = 0
            self.is_jumping = False

# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)

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
        clock = pygame.time.Clock()
        game_over = False
        last_obstacle_time = pygame.time.get_ticks()

        # Group for obstacles
        obstacles = pygame.sprite.Group()

        player = Player()
        while True:
            if not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # Update player
                player.update()

                # Add obstacles and update
                if pygame.time.get_ticks() - last_obstacle_time > 450:
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
                pygame.draw.rect(screen, BLUE, player)
                obstacles.draw(screen)

                # Display obstacle count
                score_text = font.render(f"Score: {player.score}", True, BLACK)
                screen.blit(score_text, (10, 10))

                pygame.display.update()
                clock.tick(FPS)
                obstacle = Obstacle(player)

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

                    # Group for obstacles
                    obstacles = pygame.sprite.Group()

                    player = Player()
                pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.game_loop()