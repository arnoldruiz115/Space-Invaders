import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, screen, x, y):
        super(Explosion, self).__init__()
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

    def update(self):
        self.screen.blit(self.explosion2, (self.x, self.y))
        pygame.display.update()
