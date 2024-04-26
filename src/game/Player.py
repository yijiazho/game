import pygame
from Bullet import Bullet

class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy, screen_width, screen_height):
        self.x += dx
        self.y += dy
        # Boundary check
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

    def fire(self, bullet_image):
        # Fire a bullet from the center top of the player
        new_bullet = Bullet(self.x + self.width // 2 - bullet_image.get_width() // 2, self.y, bullet_image)
        new_bullet.fire(self.x + self.width // 2 - bullet_image.get_width() // 2, self.y)
        return new_bullet
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
