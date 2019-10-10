import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/mothership.png')
        self.image = pygame.transform.scale(self.image, (64, 28))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x > self.ai_settings.screen_width:
            self.kill()
        self.rect.x += self.ai_settings.alien_speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)
