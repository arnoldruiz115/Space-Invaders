import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from explosion import Explosion
from ufo import UFO
import random


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    offset = 0
    if row_number < 3:
        alien = Alien(ai_settings, screen, "alien2")
        offset = 2
    else:
        alien = Alien(ai_settings, screen, "alien1")
    if row_number == 0:
        alien = Alien(ai_settings, screen, "alien3")
        offset = 8
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number + offset
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number + 100
    aliens.add(alien)


def update_ufos(ufos, ai_settings, screen):
    current_tick = pygame.time.get_ticks()
    if current_tick - ai_settings.start_tick > ai_settings.spawn_time:
        ai_settings.spawn_time = random.randint(20000, 50000)
        ai_settings.start_tick = current_tick
        create_ufo(ai_settings, screen, ufos)
    ufos.update()


def create_ufo(ai_settings, screen, ufos):
    ufo = UFO(ai_settings, screen)
    ufo.rect.x = -10
    ufo.rect.y = 80
    ufos.add(ufo)


def create_fleet(ai_settings, screen, aliens):
    for row_number in range(5):
        for alien_number in range(11):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        ship.moving_left = False
    elif event.key == pygame.K_LEFT:
        ship.moving_right = False
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, play_button=play_button,
                              ship=ship, aliens=aliens, bullets=bullets, mouse_x=mouse_x, mouse_y=mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            aliens.empty()
            bullets.empty()
            create_fleet(ai_settings, screen, aliens)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, explosions, ufos):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    explosions.draw(screen)
    ufos.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    sb.show_score()
    if not stats.game_active:
        draw_main_screen(screen)
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets, explosions, ufos):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, stats, sb, aliens, bullets, explosions)
    check_ufo_bullet_collision(ufos=ufos, bullets=bullets, stats=stats, sb=sb)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, aliens, bullets, explosions):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    alien_points = 0
    if collisions:
        for alien in collisions:
            # Create new explosion
            explosion = Explosion(screen=screen, x=alien.rect.x, y=alien.rect.y, ai_settings=ai_settings)
            explosions.add(explosion)
            alien_points += ai_settings.alien_points[alien.alien_type]
        for aliens in collisions.values():
            stats.score += alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens)


def check_ufo_bullet_collision(ufos, bullets, stats, sb):
    collision = pygame.sprite.groupcollide(ufos, bullets, False, True)
    ufo_value = 0
    if collision:
        for ufo in collision:
            ufo.destroy_ufo()
            ufo_value = ufo.point_value
            print("Ufo dead at {}, {}. Points = {}".format(ufo.rect.x, ufo.rect.y, ufo.point_value))
        for ufos in collision.values():
            stats.score += ufo_value * len(ufos)
            sb.prep_score()
        check_high_score(stats, sb)


def update_explosions(explosions):
    explosions.update()


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, sb, aliens, ship, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            # return because if multiple aliens touch the bottom, multiple lives are lost
            return


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def draw_main_screen(screen):
    screen.fill((0, 0, 0))
