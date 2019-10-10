import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen, type):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_type = type

        # Images for the first alien type
        self.alien_one = []
        self.one_a = pygame.image.load('images/alien1a.png')
        self.one_a = pygame.transform.scale(self.one_a, (48, 32))
        self.one_b = pygame.image.load('images/alien1b.png')
        self.one_b = pygame.transform.scale(self.one_b, (48, 32))
        self.alien_one.append(self.one_a)
        self.alien_one.append(self.one_b)

        # Images for the second alien type
        self.alien_two = []
        self.two_a = pygame.image.load('images/alien2a.png')
        self.two_a = pygame.transform.scale(self.two_a, (44, 32))
        self.two_b = pygame.image.load('images/alien2b.png')
        self.two_b = pygame.transform.scale(self.two_b, (44, 32))
        self.alien_two.append(self.two_a)
        self.alien_two.append(self.two_b)

        # Images for the third alien type
        self.alien_three = []
        self.three_a = pygame.image.load('images/alien3a.png')
        self.three_a = pygame.transform.scale(self.three_a, (32, 32))
        self.three_b = pygame.image.load('images/alien3b.png')
        self.three_b = pygame.transform.scale(self.three_b, (32, 32))
        self.alien_three.append(self.three_a)
        self.alien_three.append(self.three_b)

        # Dictionary to refer to the aliens images
        self.types = {
            "alien1": self.alien_one,
            "alien2": self.alien_two,
            "alien3": self.alien_three
        }

        self.rect = self.one_a.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.image_index = 0
        self.image = self.types[self.alien_type][self.image_index]

        self.start_tick = pygame.time.get_ticks()
        self.animation_time = 800

        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.animate()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def animate(self):
        current_tick = pygame.time.get_ticks()
        if current_tick - self.start_tick > self.animation_time:
            self.start_tick = current_tick
            self.image_index += 1
            if self.image_index >= len(self.types[self.alien_type]):
                self.image_index = 0
        self.image = self.types[self.alien_type][self.image_index]
