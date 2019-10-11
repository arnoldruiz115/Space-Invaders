import pygame.sysfont


class Button:
    def __init__(self, screen, msg, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x = x
        self.y = y

        self.width, self.height = 200, 50
        self.button_color = (37, 191, 109)
        self.text_color = (20, 44, 71)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.prep_msg(msg)
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
