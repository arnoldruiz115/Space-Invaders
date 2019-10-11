import pygame
from pygame.sprite import Sprite
from PIL import Image


class Bunker(Sprite):
    def __init__(self, screen, x, y):
        super(Bunker, self).__init__()
        self.screen = screen
        self.x = x
        self.y = y

        self.im = Image.open('images/bunker.png')
        self.raw_string = self.im.tobytes("raw", "RGBA")

        # self.image = pygame.image.fromstring(self.raw_string, self.im.size, "RGBA").convert_alpha()
        self.image = pygame.image.load('images/bunker.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def draw_pixels(self):
        pass
