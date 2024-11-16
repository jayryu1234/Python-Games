import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define fonts
FONT = pygame.font.SysFont('Arial', 24)

# Create sprite groups globally
all_sprites = pygame.sprite.Group()  # All game objects (player, enemies, bullets)
bullets = pygame.sprite.Group()  # Only the bullets
enemies = pygame.sprite.Group()  # All enemies

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.hp = 100
        self.attack = 10
        self.defense = 5  # Added defense attribute
        self.level = 1
        self.exp = 0
        self.is_shooting = False
        self.dash_cooldown = 0
        self.shield_active = False
        self.shield_duration = 0
        self.angle = 0

    def update(self, keys, mouse_pos):
        """Update player position, actions and aiming direction."""
        # Player movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Dash ability (Spacebar)
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if keys[pygame.K_SPACE] and self.dash_cooldown == 0:
            self.dash(keys)  # Dash when spacebar is pressed
            self.dash_cooldown = 30  # Cooldown for dash ability

        # Shield ability (Shift key)
        if self.shield_active:
            self.shield_duration -= 1
            if self.shield_duration <= 0:
                self.shield_active = False

        if keys[pygame.K_LSHIFT] and not self.shield_active:
            self.activate_shield()

        # Aim the gun towards the mouse position
        self.aim_gun(mouse_pos)

    def shoot(self):
        """Fires a bullet if not already shooting."""
        if not self.is_shooting:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.angle, self.attack)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.is_shooting = True  # Flag to indicate shooting is in progress

    def stop_shooting(self):
        """Stops shooting once the spacebar is released."""
        self.is_shooting = False

    def dash(self, keys):
        """Moves the player quickly in the direction they are currently facing."""
        if keys[pygame.K_LEFT]:
            self.rect.x -= 50
        if keys[pygame.K_RIGHT]:
            self.rect.x += 50
        if keys[pygame.K_UP]:
            self.rect.y -= 50
        if keys[pygame.K_DOWN]:
            self.rect.y += 50

    def activate_shield(self):
        """Activates the shield ability."""
        self.shield_active = True
        self.shield_duration = 120  # Shield lasts for 2 seconds

    def aim_gun(self, mouse_pos):
        """Aims the gun in the direction of the mouse."""
        dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))

    def attack_enemy(self, enemy):
        """Attack an enemy. If shield is active, damage is absorbed."""
        if self.shield_active:
            print("Player's shield absorbs the damage!")
            return 0  # No damage if shield is active
        damage = max(self.attack - enemy.defense, 0)
        enemy.hp -= damage
        return damage

    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= 100:
            self.exp -= 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.attack += 2
        self.hp += 10
        self.defense += 1  # Increase defense when leveling up
        print(f"Level up! Now level {self.level}.")

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
        health_text = FONT.render(f"HP: {self.hp}", True, WHITE)
        screen.blit(health_text, (10, 10))

        # Draw the shield if active
        if self.shield_active:
            pygame.draw.circle(screen, BLUE, self.rect.center, 60, 5)
        # Display the aiming direction (a line indicating where the player is aiming)
        pygame.draw.line(screen, WHITE, self.rect.center, pygame.mouse.get_pos(), 2)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hp = 50
        self.attack = 5
        self.defense = 2
        self.speed = 2

    def move_towards_player(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

    def attack_player(self, player):
        if player.shield_active:
            print("Player is shielded! No damage taken.")
            return 0  # No damage if the shield is active
        damage = max(self.attack - player.defense, 0)
        player.hp -= damage
        return damage

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
        health_text = FONT.render(f"HP: {self.hp}", True, WHITE)
        screen.blit(health_text, (self.rect.x, self.rect.y - 20))

# Bullet class (for the gun special move)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
        self.angle = angle
        self.damage = damage  # Bullet damage is set here

    def update(self):
        # Move the bullet in the direction of the angle
        radian = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radian)
        self.rect.y += self.speed * math.sin(radian)

        # Check for collision with enemies
        hit_enemies = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in hit_enemies:
            enemy.hp -= self.damage  # Bullet damage from the bullet object
            self.kill()  # Remove bullet on hit
            if enemy.hp <= 0:
                print(f"Enemy defeated!")
                Player.gain_exp(50)
                enemies.remove(enemy)
                all_sprites.remove(enemy)
                new_enemy = Enemy(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100))
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()

# Main game function
def game():
    # Create the screen object
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Game with Gun, Aiming, Dash, and Shield")

    # Create player and enemy group
    player = Player()
    all_sprites.add(player)

    # Create some enemies
    for _ in range(5):
        enemy = Enemy(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100))
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()  # Trigger the shooting action
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.stop_shooting()  # Stop shooting when space is released

        # Handle player input and movement
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position for aiming
        player.update(keys, mouse_pos)

        # Update bullets
        bullets.update()

        # Handle enemy movement and attacks
        for enemy in enemies:
            enemy.move_towards_player(player)
            if enemy.rect.colliderect(player.rect):
                damage = enemy.attack_player(player)
                print(f"Enemy attacks! Player's HP: {player.hp} remaining.")

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        bullets.draw(screen)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game()