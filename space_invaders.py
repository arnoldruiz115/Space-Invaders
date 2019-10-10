import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from explosion import Explosion


def run_game():
    pygame.init()
    main_clock = pygame.time.Clock()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    play_button = Button(screen, "Play")
    ship = Ship(ai_settings, screen)
    bullets = Group()
    explosion = Group()
    aliens = Group()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Main loop for the game
    while True:
        gf.check_events(ai_settings=ai_settings, screen=screen, stats=stats, ship=ship, sb=sb, play_button=play_button,
                        bullets=bullets, aliens=aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                              bullets=bullets)
            gf.update_aliens(ai_settings=ai_settings, stats=stats, screen=screen, sb=sb,
                             aliens=aliens, ship=ship, bullets=bullets)
        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship, sb=sb, aliens=aliens, bullets=bullets,
                         play_button=play_button, stats=stats)
        main_clock.tick(120)


run_game()
