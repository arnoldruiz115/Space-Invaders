import pygame
from pygame.sprite import Sprite
import random
import pygame.sysfont


class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/mothership.png')
        self.image = pygame.transform.scale(self.image, (64, 28))
        self.rect = self.image.get_rect()
        self.point_value = random.randint(5, 20) * 10
        self.destroyed = False
        self.destroy_time = None

        self.font = pygame.font.SysFont(None, 48)
        self.score_string = "{}".format(self.point_value)
        self.score_image = self.font.render(self.score_string, True, (255, 255, 255), self.ai_settings.bg_color)

        self.x = float(self.rect.x)

    def update(self):
        if self.rect.x > self.ai_settings.screen_width:
            self.kill()
        if self.destroyed:
            current_tick = pygame.time.get_ticks()
            if current_tick - self.destroy_time > 500:
                self.kill()
            self.image = self.score_image
        else:
            self.x += self.ai_settings.alien_speed_factor * self.ai_settings.speedup_scale
            self.rect.x = self.x

    def destroy_ufo(self):
        self.destroyed = True
        self.destroy_time = pygame.time.get_ticks()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
