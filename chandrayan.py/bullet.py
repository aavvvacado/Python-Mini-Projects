import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10 

    def update(self):
        self.rect.y += self.speedy
       
        if self.rect.bottom < 0:
            self.kill()
