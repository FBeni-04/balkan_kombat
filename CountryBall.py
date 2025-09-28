import Global
import random
import pygame
class CountryBall:
    def __init__(self, name, index):
        self.name = name
        self.image = pygame.image.load(f"./images/{name.lower().replace(' ', '_')}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.radius = 40
        self.speed = 5
        self.direction = -1 if index % 2 == 0 else 1
        self.x = -self.radius * 2 if self.direction == 1 else Global.WIDTH + self.radius * 2
        self.y = 100 + index * 35
        self.target_x = Global.WIDTH // 2 - 200 + (index % 6) * 70

    def update(self):
        if (self.direction == 1 and self.x < self.target_x) or (self.direction == -1 and self.x > self.target_x):
            self.x += self.speed * self.direction

    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))
