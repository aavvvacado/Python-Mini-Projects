import pygame
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))  
        self.rect = self.image.get_rect(center=(width // 2, height - 50))
        self.width = width
        self.height = height
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height

    def shoot(self, bullet_image, all_sprites, bullets):
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
