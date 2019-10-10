import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, screen, x, y, ai_settings):
        super(Explosion, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.x = x
        self.y = y
        self.alien_explosion = []
        self.explosion1 = pygame.image.load('images/explosion1.png')
        self.explosion1 = pygame.transform.scale(self.explosion1, (52, 32))
        self.explosion2 = pygame.image.load('images/explosion2.png')
        self.explosion2 = pygame.transform.scale(self.explosion2, (52, 32))
        self.alien_explosion.append(self.explosion1)
        self.alien_explosion.append(self.explosion2)

        self.frame = 0
        self.image = self.alien_explosion[self.frame]

        self.start_tick = pygame.time.get_ticks()
        self.animation_time = 50
        self.frames = 4
        self.counter = 0

    def update(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.start_tick > self.animation_time:
            if self.counter == 4:
                self.kill()
            self.counter += 1
            self.start_tick = current_tick
            self.frame += 1
            if self.frame >= len(self.alien_explosion):
                self.frame = 0
        self.image = self.alien_explosion[self.frame]
        self.x += self.ai_settings.fleet_direction * self.ai_settings.alien_speed_factor
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.update()
