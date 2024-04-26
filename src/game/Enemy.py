import pygame
import random

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed_x = 5
        self.speed_y = 2
        self.health = 100
        self.direction_change_frequency = 1000
        self.last_direction_change = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self, screen_width, change_dir=False):
        if change_dir:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
        self.x += self.speed_x * self.direction_x
        self.y += self.speed_y * self.direction_y
        # Boundary check
        if self.x <= 0 or self.x >= screen_width - self.width:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= 100:  # Restrict Y movement within top 100 pixels
            self.direction_y *= -1

    def move(self, screen_width, current_time):
        # Time-based random direction change
        if current_time - self.last_direction_change > self.direction_change_frequency:
            if random.random() < 0.5:  # 50% chance to change direction
                self.direction_x = random.choice([-1, 1])
                self.direction_y = random.choice([-1, 1])
            self.last_direction_change = current_time

        # Move enemy based on current direction
        self.x += self.speed_x * self.direction_x
        self.y += self.speed_y * self.direction_y

        # Boundary check for X
        if self.x <= 0 or self.x >= screen_width - self.width:
            self.direction_x *= -1

        # Boundary check for Y within top 100 pixels
        if self.y <= 0 or self.y >= 100:
            self.direction_y *= -1

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0 