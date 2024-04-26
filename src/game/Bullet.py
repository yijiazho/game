import pygame

class Bullet:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.state = "ready"  # can be "ready" or "fire"
        self.speed_y = -10

    def fire(self, x, y):
        self.x = x
        self.y = y
        self.state = "fire"

    def move(self):
        if self.state == "fire":
            self.y += self.speed_y
            if self.y <= 0:
                self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        if self.state == "fire":
            return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        return None
