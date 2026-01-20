#!/usr/bin/env python3
"""
Space Invaders Game
A classic arcade-style shooter game built with Pygame
"""

import pygame
import random
import sys

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


class Player(pygame.sprite.Sprite):
    """Player ship class"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        # Draw a simple ship shape
        pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 30), (50, 30)])
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
        """Create a bullet at player position"""
        return Bullet(self.rect.centerx, self.rect.top)


class Enemy(pygame.sprite.Sprite):
    """Enemy invader class"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        # Draw a simple invader shape
        pygame.draw.rect(self.image, YELLOW, (5, 5, 30, 20))
        pygame.draw.rect(self.image, RED, (10, 10, 5, 5))
        pygame.draw.rect(self.image, RED, (25, 10, 5, 5))
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
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

    def create_enemies(self):
        """Create a grid of enemies"""
        rows = 5
        cols = 10
        padding = 60
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over and not self.won:
                    # Shoot with delay
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_shot > self.shoot_delay:
                        bullet = self.player.shoot()
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
        self.screen.fill(BLACK)
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
        print("Starting Space Invaders!")
        print("Controls:")
        print("  LEFT/RIGHT arrows - Move ship")
        print("  SPACE - Shoot")
        print("  R - Restart (when game over)")
        print("  ESC - Quit")
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
