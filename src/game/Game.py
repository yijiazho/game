import pygame
import random
from Player import Player
from Enemy import Enemy
from Bullet import Bullet

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        # Load images
        self.background = pygame.image.load('./background.jpg')
        player_image = pygame.image.load('./player.png')
        self.bullet_image = pygame.image.load('./bullet.png')  # Preload bullet image
        self.enemy_image = pygame.image.load('./ufo.png')

        # Create game objects
        self.player = Player(370, 480, player_image)
        self.enemies = []
        self.bullets = []

        # Timed enemy spawning
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_interval = 2000

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Let the player fire a bullet
                    new_bullet = self.player.fire(self.bullet_image)
                    self.bullets.append(new_bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(0, -5, 800, 600)
        if keys[pygame.K_s]:
            self.player.move(0, 5, 800, 600)
        if keys[pygame.K_a]:
            self.player.move(-5, 0, 800, 600)
        if keys[pygame.K_d]:
            self.player.move(5, 0, 800, 600)

    def update(self):
        current_time = pygame.time.get_ticks()

        # Spawn new enemies
        if current_time - self.last_spawn > self.spawn_interval:
            new_enemy = Enemy(random.randint(0, 800 - 64), 100, self.enemy_image)
            self.enemies.append(new_enemy)
            self.last_spawn = current_time

        # Update enemies
        for enemy in self.enemies:
            enemy.move(self.screen.get_width(), current_time)

        # Update bullets
        for bullet in self.bullets:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # Collision checks
        for enemy in self.enemies[:]:
            if self.player.get_rect().colliderect(enemy.get_rect()):
                self.game_over()
            for bullet in self.bullets[:]:
                if bullet.get_rect() and bullet.get_rect().colliderect(enemy.get_rect()):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        pygame.display.update()

    def game_over(self):
        self.running = False
        print("Game Over")

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
