import pygame
import random
from Enemy import Enemy
from Bullet import Bullet

class Boss(Enemy):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.speed_x = 8  
        self.speed_y = 4
        self.health = 300

    def move(self, screen_width, screen_height, current_time):
        # Boss movement logic, moves faster and without random direction changes
        self.x += self.speed_x * self.direction_x
        self.y += self.speed_y * self.direction_y

        # Boundary check, bounces off the edges
        if self.x <= 0 or self.x >= screen_width - self.width:
            self.direction_x *= -1
        if self.y <= 0 or self.y >= screen_height - self.height:
            self.direction_y *= -1

    def fire(self, bullet_image):
        # Boss fires a bullet from its position
        new_bullet = Bullet(self.x + self.width // 2 - bullet_image.get_width() // 2, self.y + self.height, bullet_image)
        new_bullet.fire(self.x + self.width // 2 - bullet_image.get_width() // 2, self.y + self.height)
        return new_bullet
