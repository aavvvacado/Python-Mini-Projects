import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, initial_speed, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = initial_speed
        self.width = width
        self.height = height

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > self.height:
            self.rect.x = random.randint(0, self.width - self.rect.width)
            self.rect.y = random.randint(-100, -40)

    def increase_speed(self):
        self.speedy += 0.5
