import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -3  
        if keys[pygame.K_RIGHT]:
            self.speedx = 3  
        self.rect.x += self.speedx
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, bullet_img, all_sprites, bullets):
        bullet = Bullet(bullet_img, self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
