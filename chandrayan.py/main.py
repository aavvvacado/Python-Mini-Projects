import pygame
import sys
import random
import os
from player import Player
from enemy import Enemy
from bullet import Bullet

# Initialize Pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chandrayan")


try:
    player_img = pygame.image.load("player.png").convert()
    enemy_img = pygame.image.load("enemy.png").convert()
    bullet_img = pygame.image.load("bullet.png").convert()
    player_img.set_colorkey((0, 0, 0))  
    enemy_img.set_colorkey((0, 0, 0))
    bullet_img.set_colorkey((0, 0, 0))
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()
except FileNotFoundError as e:
    print(f"File not found: {e}")
    pygame.quit()
    sys.exit()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

#player
player = Player(player_img, WIDTH, HEIGHT)
all_sprites.add(player)

#states
START, PLAYING, GAME_OVER = 0, 1, 2
game_state = START
score = 0
high_score = 0
font = pygame.font.SysFont(None, 36)

#High score file
HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    global high_score
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            high_score = int(file.read().strip())
    else:
        high_score = 0

def save_high_score():
    global score, high_score
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(high_score))

def show_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def start_screen():
    screen.fill(BLACK)
    show_text("Space Shooter", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    show_text(f"High Score: {high_score}", 36, GREEN, WIDTH // 2, HEIGHT // 2 - 50)
    show_text("Press any key to start", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    show_text("How to Play: Use arrow keys to move, Space to shoot", 24, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    wait_for_key()

def game_over_screen():
    screen.fill(BLACK)
    show_text("GAME OVER", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    show_text(f"Score: {score}", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    show_text("Press any key to restart", 36, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    save_high_score()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def create_enemies(num):
    for _ in range(num):
        x = random.randint(0, WIDTH - 40)  
        y = random.randint(-100, -40)  
        enemy = Enemy(enemy_img, x, y, initial_speed=1.4) 
        all_sprites.add(enemy)
        enemies.add(enemy)

def game_loop():
    global score, game_state, high_score
    score = 0
    game_state = PLAYING

    all_sprites.empty()
    bullets.empty()
    enemies.empty()
    all_sprites.add(player)
    create_enemies(8)

    while game_state == PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(bullet_img, all_sprites, bullets)

        all_sprites.update()

        # Create enemies 
        if len(enemies) < 8:
            x = random.randint(0, WIDTH - 40)  
            y = random.randint(-100, -40)  
            enemy = Enemy(enemy_img, x, y, initial_speed=2) 
            all_sprites.add(enemy)
            enemies.add(enemy)

       
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            if score % 10 == 0: 
                for enemy in enemies:
                    enemy.increase_speed()

       
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_state = GAME_OVER

        
        screen.fill(BLACK)
        all_sprites.draw(screen)
        show_text(f"Score: {score}", 36, WHITE, 70, 10)
        show_text(f"High Score: {high_score}", 36, GREEN if score < high_score else WHITE, WIDTH - 150, 10)
        pygame.display.flip()


load_high_score()
while True:
    if game_state == START:
        start_screen()
        game_loop()
    elif game_state == GAME_OVER:
        game_over_screen()
        game_loop()
