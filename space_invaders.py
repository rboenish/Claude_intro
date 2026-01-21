#!/usr/bin/env python3
"""
Space Invaders Game - Political Edition
A classic arcade-style shooter game built with Pygame
Featuring Zohran Mamdani vs. Political Opponents
"""

import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Game settings
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 1
ENEMY_DROP = 30
ENEMY_BULLET_SPEED = 4
ENEMY_SHOOT_CHANCE = 0.001

# Image paths (images in images/ folder)
PLAYER_IMAGE = "images/zohran_mamdani.jpg.webp"
ENEMY_IMAGES = [
    "images/andrew_cuomo.jpg",
    "images/donald_trump.jpg",
    "images/jd_vance.jpg"
]


def create_hammer_sickle_background(width, height):
    """Create a faded hammer and sickle background like the Soviet logo"""
    surface = pygame.Surface((width, height))
    surface.fill(BLACK)

    # Faded dark red/maroon color for the symbol
    FADED_RED = (50, 12, 12)

    center_x, center_y = width // 2, height // 2

    # Scale factor for the whole symbol
    scale = 1.5

    # Draw sickle blade (crescent moon shape using two overlapping circles)
    sickle_outer_radius = int(100 * scale)
    sickle_inner_radius = int(75 * scale)
    sickle_center_x = center_x - int(30 * scale)
    sickle_center_y = center_y - int(20 * scale)

    # Draw outer circle of sickle
    pygame.draw.circle(surface, FADED_RED, (sickle_center_x, sickle_center_y), sickle_outer_radius)
    # Cut out inner circle to make crescent (use black)
    pygame.draw.circle(surface, BLACK, (sickle_center_x + int(25 * scale), sickle_center_y - int(15 * scale)), sickle_inner_radius)

    # Cut out bottom portion to make it a sickle shape (not full crescent)
    pygame.draw.rect(surface, BLACK, (center_x - int(150 * scale), center_y + int(20 * scale), int(300 * scale), int(150 * scale)))
    # Cut out left portion
    pygame.draw.rect(surface, BLACK, (center_x - int(200 * scale), center_y - int(150 * scale), int(100 * scale), int(300 * scale)))

    # Draw sickle handle
    handle_points = [
        (center_x - int(60 * scale), center_y + int(15 * scale)),
        (center_x - int(50 * scale), center_y + int(20 * scale)),
        (center_x - int(90 * scale), center_y + int(80 * scale)),
        (center_x - int(100 * scale), center_y + int(75 * scale)),
    ]
    pygame.draw.polygon(surface, FADED_RED, handle_points)

    # Draw hammer handle (diagonal)
    hammer_handle_points = [
        (center_x + int(10 * scale), center_y - int(10 * scale)),
        (center_x + int(20 * scale), center_y - int(5 * scale)),
        (center_x + int(80 * scale), center_y + int(90 * scale)),
        (center_x + int(70 * scale), center_y + int(95 * scale)),
    ]
    pygame.draw.polygon(surface, FADED_RED, hammer_handle_points)

    # Draw hammer head (rotated rectangle at top of handle)
    hammer_head_points = [
        (center_x - int(25 * scale), center_y - int(35 * scale)),
        (center_x + int(45 * scale), center_y + int(5 * scale)),
        (center_x + int(35 * scale), center_y + int(18 * scale)),
        (center_x - int(35 * scale), center_y - int(22 * scale)),
    ]
    pygame.draw.polygon(surface, FADED_RED, hammer_head_points)

    return surface


def load_and_scale_image(image_path, width, height, fallback_color=None):
    """Load an image and scale it, or create a colored surface if not found"""
    try:
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            # Convert to surface with alpha
            image = image.convert_alpha()
            # Scale to desired size
            image = pygame.transform.scale(image, (width, height))
            return image, True
    except Exception as e:
        print(f"Could not load image {image_path}: {e}")

    # Fallback to colored surface
    surface = pygame.Surface((width, height))
    if fallback_color:
        surface.fill(fallback_color)
    return surface, False


class Player(pygame.sprite.Sprite):
    """Player ship class - Zohran Mamdani"""
    def __init__(self):
        super().__init__()
        # Try to load Zohran Mamdani's image
        self.image, loaded = load_and_scale_image(PLAYER_IMAGE, 60, 60, GREEN)

        if not loaded:
            # Fallback: Draw a simple ship shape
            pygame.draw.polygon(self.image, WHITE, [(30, 0), (0, 60), (60, 60)])

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED

    def update(self):
        """Update player position based on key presses"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        """Create three bullets at player position with vertical offset"""
        return [
            Bullet(self.rect.centerx, self.rect.top),
            Bullet(self.rect.centerx, self.rect.top + 10),
            Bullet(self.rect.centerx, self.rect.top + 20)
        ]


class Enemy(pygame.sprite.Sprite):
    """Enemy invader class - Political opponents"""
    def __init__(self, x, y):
        super().__init__()
        # Randomly choose one of the enemy images
        enemy_image_path = random.choice(ENEMY_IMAGES)
        self.image, loaded = load_and_scale_image(enemy_image_path, 40, 40, RED)

        if not loaded:
            # Fallback: Draw a simple invader shape
            pygame.draw.rect(self.image, YELLOW, (4, 4, 32, 32))
            pygame.draw.rect(self.image, RED, (12, 12, 8, 8))
            pygame.draw.rect(self.image, RED, (20, 12, 8, 8))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        """Create an enemy bullet"""
        return EnemyBullet(self.rect.centerx, self.rect.bottom)


class Bullet(pygame.sprite.Sprite):
    """Player bullet class"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -BULLET_SPEED

    def update(self):
        """Move bullet upward"""
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Enemy bullet class"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = ENEMY_BULLET_SPEED

    def update(self):
        """Move bullet downward"""
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Space Invaders - Political Edition")
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.won = False

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)

        # Game state
        self.score = 0
        self.enemy_direction = 1
        self.last_shot = 0
        self.shoot_delay = 500  # milliseconds

        # Create enemies
        self.create_enemies()

        # Font
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        # Create background with hammer and sickle
        self.background = create_hammer_sickle_background(SCREEN_WIDTH, SCREEN_HEIGHT)

    def create_enemies(self):
        """Create a grid of enemies"""
        rows = 4
        cols = 8
        padding = 55
        offset_x = 80
        offset_y = 60

        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * padding
                y = offset_y + row * 50
                enemy = Enemy(x, y)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

    def update_enemies(self):
        """Update enemy positions and handle movement"""
        # Check if any enemy hit the edge
        hit_edge = False
        for enemy in self.enemies:
            if (enemy.rect.right >= SCREEN_WIDTH and self.enemy_direction > 0) or \
               (enemy.rect.left <= 0 and self.enemy_direction < 0):
                hit_edge = True
                break

        # If hit edge, reverse direction and move down
        if hit_edge:
            self.enemy_direction *= -1
            for enemy in self.enemies:
                enemy.rect.y += ENEMY_DROP

                # Check if enemies reached player
                if enemy.rect.bottom >= self.player.rect.top:
                    self.game_over = True

        # Move enemies horizontally
        for enemy in self.enemies:
            enemy.rect.x += self.enemy_direction * ENEMY_SPEED

            # Random shooting
            if random.random() < ENEMY_SHOOT_CHANCE:
                bullet = enemy.shoot()
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)

    def handle_collisions(self):
        """Handle all collision detection"""
        # Player bullets hitting enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 10

        # Enemy bullets hitting player
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.game_over = True

        # Check win condition
        if len(self.enemies) == 0:
            self.won = True

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.width = event.w
                self.height = event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.background = create_hammer_sickle_background(self.width, self.height)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and not self.won:
                    # Shoot with delay
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_shot > self.shoot_delay:
                        bullets = self.player.shoot()
                        for bullet in bullets:
                            self.bullets.add(bullet)
                            self.all_sprites.add(bullet)
                        self.last_shot = current_time
                elif event.key == pygame.K_r and (self.game_over or self.won):
                    # Restart game
                    self.__init__()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game state"""
        if not self.game_over and not self.won:
            self.all_sprites.update()
            self.update_enemies()
            self.handle_collisions()

    def draw(self):
        """Draw everything"""
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over or win message
        if self.game_over:
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to Restart or ESC to Quit", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)

        elif self.won:
            win_text = self.large_font.render("YOU WIN!", True, GREEN)
            score_display = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press R to Restart or ESC to Quit", True, WHITE)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            score_rect = score_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(win_text, win_rect)
            self.screen.blit(score_display, score_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        print("=" * 60)
        print("Space Invaders - Political Edition")
        print("=" * 60)
        print("Play as Zohran Mamdani defending against:")
        print("  - Andrew Cuomo")
        print("  - Donald Trump")
        print("  - JD Vance")
        print()
        print("Controls:")
        print("  LEFT/RIGHT arrows - Move")
        print("  SPACE - Shoot (triple shot!)")
        print("  R - Restart (when game over)")
        print("  ESC - Quit")
        print()
        print("Images loaded from root directory:")
        print("=" * 60)
        print()

        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()

