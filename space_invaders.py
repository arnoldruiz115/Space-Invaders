import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    main_clock = pygame.time.Clock()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    play_button = Button(screen, "Play", ai_settings.screen_width / 2, 700)
    scores_button = Button(screen, "High Scores", ai_settings.screen_width / 2, 800)
    back_button = Button(screen, "Back", 150, 75)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    lasers = Group()
    explosions = Group()
    ufos = Group()
    bunkers = Group()
    aliens = Group()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    gf.create_fleet(ai_settings, screen, aliens)

    # Main loop for the game
    while True:
        gf.check_events(ai_settings=ai_settings, screen=screen, stats=stats, ship=ship, sb=sb, play_button=play_button,
                        bullets=bullets, aliens=aliens, score_button=scores_button,
                        back_button=back_button, bunkers=bunkers)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, aliens=aliens,
                              bullets=bullets, explosions=explosions, ufos=ufos, bunkers=bunkers)
            gf.update_aliens(ai_settings=ai_settings, stats=stats, screen=screen, sb=sb,
                             aliens=aliens, ship=ship, bullets=bullets, lasers=lasers)
            gf.update_explosions(explosions=explosions)
            gf.update_ufos(ufos=ufos, screen=screen, ai_settings=ai_settings)
            gf.update_lasers(lasers=lasers)
            gf.update_bunkers(bunkers=bunkers)

        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship, sb=sb, aliens=aliens, bullets=bullets,
                         play_button=play_button, stats=stats, explosions=explosions, ufos=ufos,
                         score_button=scores_button, back_button=back_button, lasers=lasers, bunkers=bunkers)
        main_clock.tick(120)


run_game()
