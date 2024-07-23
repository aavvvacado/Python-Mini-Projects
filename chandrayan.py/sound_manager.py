
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.shoot_sound = pygame.mixer.Sound("shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("explosion.wav")
        pygame.mixer.music.load("background.ogg")

    def play_shoot(self):
        self.shoot_sound.play()

    def play_explosion(self):
        self.explosion_sound.play()

    def play_background(self):
        pygame.mixer.music.play(loops=-1)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
