import pygame
import sys
import random
import os
from player import Player
from enemy import Enemy
from bullet import Bullet
from settings import Settings
from sound_manager import SoundManager

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chandrayan")




# Load Images
try:
    player_img = pygame.image.load("player.png").convert_alpha()
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    bullet_img = pygame.image.load("bullet.png").convert_alpha()
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()
player = Player(player_img, WIDTH, HEIGHT)

# Set up icon
icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize game objects
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(player_img, WIDTH, HEIGHT)
all_sprites.add(player)

# Initialize sound manager and settings
sound_manager = SoundManager()
settings = Settings()

# Game states
START, SETTINGS, DIFFICULTY, PLAYING, GAME_OVER = 0, 1, 2, 3, 4
game_state = START
score = 0
high_score = 0
font = pygame.font.SysFont(None, 36)

# High score file
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
    show_text("CHANDRAYAN", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    show_text(f"High Score: {high_score}", 36, GREEN, WIDTH // 2, HEIGHT // 2 - 50)
    show_text("Press Any Key to Start", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    show_text("Press S for Settings", 24, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
    
    pygame.display.flip()

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
            show_text(f"{option}: {int(value*100) if option == 'Volume' else value}", 36, color, WIDTH // 2, HEIGHT // 2 - 50 + i * 50)
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
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
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
                elif event.key == pygame.K_RETURN:
                    return options[current_selection].lower()

def game_over_screen():
    screen.fill(BLACK)
    show_text("GAME OVER", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    show_text(f"Score: {score}", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    show_text("Press Any Key to Restart", 36, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
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

def create_enemies(num, speed):
    for _ in range(num):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-100, -40)
        enemy = Enemy(enemy_img, x, y, initial_speed=speed, width=WIDTH, height=HEIGHT)
        all_sprites.add(enemy)
        enemies.add(enemy)


def game_loop(difficulty):
    global score, game_state, high_score

    # Reset score at the start of the game loop
    score = 0

    # Set difficulty parameters
    if difficulty == 'easy':
        enemy_speed = 1
        num_enemies = 5
    elif difficulty == 'medium':
        enemy_speed = 2
        num_enemies = 8
    elif difficulty == 'hard':
        enemy_speed = 3
        num_enemies = 12

    game_state = PLAYING

    all_sprites.empty()
    bullets.empty()
    enemies.empty()

    # Create enemies based on difficulty
    create_enemies(num_enemies, enemy_speed)

    while game_state == PLAYING:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(bullet_img, player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    sound_manager.play_bullet()

        # Update
        all_sprites.update()
        player.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 1
            sound_manager.play_explosion()
            enemy = Enemy(enemy_img, random.randint(0, WIDTH - 40), random.randint(-100, -40), initial_speed=enemy_speed)
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check for enemy-player collisions
        if pygame.sprite.spritecollideany(player, enemies):
            sound_manager.play_explosion()
            game_state = GAME_OVER

        # Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)
        show_text(f"Score: {score}", 36, WHITE, 100, 10)
        show_text(f"High Score: {high_score}", 36, WHITE, WIDTH - 200, 10)
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    # Save high score and display game over screen only once after exiting the game loop
    save_high_score()
    game_over_screen()
if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up display
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chandrayan")

    # Load Images
    try:
        player_img = pygame.image.load("player.png").convert_alpha()
        enemy_img = pygame.image.load("enemy.png").convert_alpha()
        bullet_img = pygame.image.load("bullet.png").convert_alpha()
    except pygame.error as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        sys.exit()

    # Set up icon
    icon = pygame.image.load("player.png")
    pygame.display.set_icon(icon)

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    # Initialize game objects
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(player_img, WIDTH, HEIGHT)
    all_sprites.add(player)

    # Initialize sound manager and settings
    sound_manager = SoundManager()
    settings = Settings()

    # Game states
    START, SETTINGS, DIFFICULTY, PLAYING, GAME_OVER = 0, 1, 2, 3, 4
    game_state = START
    score = 0
    high_score = 0
    font = pygame.font.SysFont(None, 36)

    # High score file
    HIGH_SCORE_FILE = "high_score.txt"

    load_high_score()
    sound_manager.play_background()

    while True:
        if game_state == START:
            start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    game_state = DIFFICULTY
        elif game_state == SETTINGS:
            settings_screen()
            game_state = START
        elif game_state == DIFFICULTY:
            difficulty = difficulty_screen()
            game_loop(difficulty)
        elif game_state == GAME_OVER:
            game_over_screen()
            game_state = START
        pygame.display.flip()
