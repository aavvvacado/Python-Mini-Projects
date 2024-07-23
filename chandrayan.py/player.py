import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speedx = 0
        self.screen_width = screen_width  # Store screen_width as an attribute

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -3  # Adjust speed for sensitivity
        if keys[pygame.K_RIGHT]:
            self.speedx = 3
        self.rect.x += self.speedx
        if self.rect.right > self.screen_width:  # Use self.screen_width instead of screen_width
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, bullet_image, all_sprites, bullets):
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
