import pygame

class Settings:
    def __init__(self):
        self.volume = 0.5
        self.sensitivity = 3

    def show_settings(self, screen, width, height):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)
        volume_text = font.render(f"Volume: {self.volume}", True, (255, 255, 255))
        sensitivity_text = font.render(f"Sensitivity: {self.sensitivity}", True, (255, 255, 255))
        screen.blit(volume_text, (width // 2 - volume_text.get_width() // 2, height // 2 - 50))
        screen.blit(sensitivity_text, (width // 2 - sensitivity_text.get_width() // 2, height // 2 + 50))
        pygame.display.flip()

    def adjust_volume(self, increase=True):
        if increase:
            self.volume = min(1, self.volume + 0.1)
        else:
            self.volume = max(0, self.volume - 0.1)

    def adjust_sensitivity(self, increase=True):
        if increase:
            self.sensitivity = min(10, self.sensitivity + 1)
        else:
            self.sensitivity = max(1, self.sensitivity - 1)
