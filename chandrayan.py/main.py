import pygame
import sys
import random
import os
from player import Player
from enemy import Enemy
from bullet import Bullet
from settings import Settings
from sound_manager import SoundManager


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chandrayan")


try:
    player_img = pygame.image.load("player.png").convert_alpha()
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    bullet_img = pygame.image.load("bullet.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (50, 50))  # Resize spaceship
    enemy_img = pygame.transform.scale(enemy_img, (100, 75))    # Resize enemies
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()


icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(player_img, WIDTH, HEIGHT)
all_sprites.add(player)


sound_manager = SoundManager()
settings = Settings()

# Game states
START, SETTINGS, DIFFICULTY, PLAYING, GAME_OVER = 0, 1, 2, 3, 4
game_state = START
score = 0
high_score = 0
font = pygame.font.SysFont(None, 36)


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
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

def start_screen():
    screen.fill(BLACK)
    title_rect = show_text("CHANDRAYAN", 80, WHITE, WIDTH // 2, HEIGHT // 6)
    high_score_rect = show_text(f"High Score: {high_score}", 36, GREEN, WIDTH // 2, HEIGHT // 4 + 50)
    start_rect = show_text("Start Game", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    settings_rect = show_text("Settings", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()
    return title_rect, high_score_rect, start_rect, settings_rect

def settings_screen():
    options = ["Volume", "Sensitivity"]
    current_selection = 0
    adjusting = True

    while adjusting:
        screen.fill(BLACK)
        show_text("Settings", 64, WHITE, WIDTH // 2, HEIGHT // 4)
        for i, option in enumerate(options):
            color = GREEN if i == current_selection else WHITE
            value = settings.volume if option == "Volume" else settings.sensitivity
            show_text(f"{option}: {int(value * 100) if option == 'Volume' else value}", 36, color, WIDTH // 2, HEIGHT // 2 - 50 + i * 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(options)
                elif event.key == pygame.K_LEFT:
                    if options[current_selection] == "Volume":
                        settings.adjust_volume(increase=False)
                    else:
                        settings.adjust_sensitivity(increase=False)
                    sound_manager.set_volume(settings.volume)
                elif event.key == pygame.K_RIGHT:
                    if options[current_selection] == "Volume":
                        settings.adjust_volume(increase=True)
                    else:
                        settings.adjust_sensitivity(increase=True)
                    sound_manager.set_volume(settings.volume)
                elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    adjusting = False

def difficulty_screen():
    options = ["Easy", "Medium", "Hard"]
    current_selection = 0
    selecting = True

    while selecting:
        screen.fill(BLACK)
        show_text("Select Difficulty", 64, WHITE, WIDTH // 2, HEIGHT // 4)
        for i, option in enumerate(options):
            color = GREEN if i == current_selection else WHITE
            show_text(option, 36, color, WIDTH // 2, HEIGHT // 2 - 50 + i * 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    return options[current_selection].lower()

def create_enemies(num_enemies, speed):
    enemy_width = enemy_img.get_rect().width
    enemy_height = enemy_img.get_rect().height

    
    if enemy_width > WIDTH or enemy_height > HEIGHT:
        print("Error: Enemy dimensions are larger than screen dimensions.")
        return
    
    for _ in range(num_enemies):
        x = random.randint(0, max(0, WIDTH - enemy_width))
        y = random.randint(-enemy_height * 2, -enemy_height)
        
        # Debug print to check the generated positions
        print(f"Generated Enemy Position - X: {x}, Y: {y}")

        enemy = Enemy(enemy_img, x, y, speed, WIDTH, HEIGHT)
        all_sprites.add(enemy)
        enemies.add(enemy)

def game_loop(difficulty):
    global score, game_state, high_score

    
    score = 0

    
    if difficulty == 'easy':
        base_enemy_speed = 1
        base_num_enemies = 5
    elif difficulty == 'medium':
        base_enemy_speed = 2
        base_num_enemies = 8
    elif difficulty == 'hard':
        base_enemy_speed = 3
        base_num_enemies = 12
    else:
        print(f"Invalid difficulty: {difficulty}")
        return

    game_state = PLAYING
    level = 1

    all_sprites.empty()
    bullets.empty()
    enemies.empty()

    player = Player(player_img, WIDTH, HEIGHT)
    all_sprites.add(player)

    create_enemies(base_num_enemies, base_enemy_speed)

    sound_manager.play_background()
    sound_manager.set_volume(settings.volume)

    while game_state == PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(bullet_img, all_sprites, bullets)

        # Update
        all_sprites.update()

        # Check collisions
        if pygame.sprite.spritecollideany(player, enemies):
            game_state = GAME_OVER

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if hits:
                bullet.kill()
                score += 10

        
        screen.fill(BLACK)
        all_sprites.draw(screen)
        show_text(f"Score: {score}", 36, WHITE, WIDTH // 2, 20)
        pygame.display.flip()

        # Regenerate enemies after level
        if not enemies:
            level += 1
            num_enemies = base_num_enemies + 2 * (level - 1)
            enemy_speed = base_enemy_speed + 0.5 * (level - 1)
            
            # Debug prints
            print(f"Level: {level}, Number of Enemies: {num_enemies}, Enemy Speed: {enemy_speed}")
            
            create_enemies(num_enemies, enemy_speed)

        
        pygame.time.Clock().tick(60)

# Main Game Loop
load_high_score()

current_selection = 0
menu_options = ["Start Game", "Settings"]
while True:
    if game_state == START:
        title_rect, high_score_rect, start_rect, settings_rect = start_screen()
        sound_manager.play_background()
        while game_state == START:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        current_selection = (current_selection - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        current_selection = (current_selection + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if current_selection == 0:
                            game_state = DIFFICULTY
                        elif current_selection == 1:
                            game_state = SETTINGS
            screen.fill(BLACK)
            show_text("CHANDRAYAN", 80, WHITE, WIDTH // 2, HEIGHT // 4)
            show_text(f"High Score: {high_score}", 36, GREEN, WIDTH // 2, HEIGHT // 2 - 50)
            for i, option in enumerate(menu_options):
                color = GREEN if i == current_selection else WHITE
                show_text(option, 36, color, WIDTH // 2, HEIGHT // 2 + i * 50)
            pygame.display.flip()
    elif game_state == SETTINGS:
        settings_screen()
        game_state = START
    elif game_state == DIFFICULTY:
        difficulty = difficulty_screen()
        if difficulty:  
            game_loop(difficulty)
        save_high_score()
        game_state = GAME_OVER
    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        show_text(f"Game Over! Score: {score}", 64, WHITE, WIDTH // 2, HEIGHT // 2)
        show_text(f"High Score: {high_score}", 36, GREEN, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()
        pygame.time.wait(3000)
        game_state = START
