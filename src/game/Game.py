import pygame
import random
from Player import Player
from Enemy import Enemy
from Bullet import Bullet
from Boss import Boss

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        # Load images
        self.background = pygame.image.load('./background.jpg')
        player_image = pygame.image.load('./player.png')
        self.bullet_image = pygame.image.load('./bullet.png')
        self.enemy_image = pygame.image.load('./ufo.png')
        self.boss_image = pygame.image.load('./boss.png')

        # Create game objects
        self.player = Player(370, 480, player_image)
        self.enemies = []
        self.bullets = []

        self.score = 0

        # Font for displaying the score
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)

        self.enemy_count = 0  
        self.boss_count = 0
        self.boss_spawn_threshold = 10

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
            enemy.move(self.screen.get_width(), self.screen.get_height(), current_time)

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
                    self.bullets.remove(bullet)

                    if enemy.take_damage(100):
                        self.enemies.remove(enemy)
                        if isinstance(enemy, Boss):
                            self.score += 100
                            self.boss_count -= 1
                        else:  
                            self.enemy_count += 1
                            self.score += 10

                    if self.enemy_count % self.boss_spawn_threshold == 0 and self.boss_count == 0:
                        self.spawn_boss()
                    break

    def spawn_boss(self):
        # Spawn a boss if the enemy count reaches a threshold
        boss = Boss(random.randint(0, 800 - 64), 100, self.boss_image)
        self.enemies.append(boss)
        self.boss_count += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Render the score
        score_text = self.font.render('Score: {}'.format(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (650, 20))  # Position the score at the top right corner

        pygame.display.update()

    def game_over(self):
        # Render the "GAME OVER" text
        game_over_font = pygame.font.SysFont('Arial', 52)  # Larger font for game over message
        game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))  # Red color for emphasis
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
    
        self.screen.blit(game_over_text, game_over_rect)  # Position the text at the center of the screen
        pygame.display.update()  # Update the display to show the text

        # Stop game updates but wait for user to close the window
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        pygame.quit()  # Quit the game properly


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
