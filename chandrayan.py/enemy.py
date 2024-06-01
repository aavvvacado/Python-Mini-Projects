import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, initial_speed=2):
        super().__init__()
        self.image = pygame.transform.scale(image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = initial_speed
        self.speedx = random.uniform(-0.5, 0.5)  

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx  
        if self.rect.top > 600 + 10 or self.rect.right < 0 or self.rect.left > 800:
            self.rect.x = random.randint(0, 800 - 40)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.uniform(1, 2) 
            self.speedx = random.uniform(-0.5, 0.5)  

    def increase_speed(self):
        self.speedy += 0.1  
