import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from explosion import Explosion
from ufo import UFO
from bunker import Bunker
import random
import json


def create_alien(ai_settings, screen, aliens, alien_number, row_number, column):
    offset = 0
    if row_number < 3:
        alien = Alien(ai_settings, screen, "alien2")
        offset = 2
    else:
        alien = Alien(ai_settings, screen, "alien1")
        if row_number == 4:
            alien.can_shoot = True
    if row_number == 0:
        alien = Alien(ai_settings, screen, "alien3")
        offset = 8
    alien.column_number = column
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number + offset
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number + 100
    aliens.add(alien)


def update_bunkers(bunkers):
    bunkers.update()


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


def create_bunkers(bunkers, screen):
    for i in range(4):
        bunker = Bunker(screen=screen, x=(150 + (200 * i)), y=600)
        bunkers.add(bunker)


def create_fleet(ai_settings, screen, aliens):
    for row_number in range(5):
        column_count = 0
        for alien_number in range(11):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, column_count)
            column_count += 1


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


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, score_button, back_button, bunkers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, play_button=play_button,
                              ship=ship, aliens=aliens, bullets=bullets,
                              mouse_x=mouse_x, mouse_y=mouse_y, bunkers=bunkers)
            check_score_button(score_button=score_button, stats=stats,
                               mouse_x=mouse_x, mouse_y=mouse_y)
            check_back_button(back_button=back_button, stats=stats, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_score_button(score_button, stats, mouse_x, mouse_y):
    button_clicked = score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        stats.score_screen_active = True


def check_back_button(back_button, stats, mouse_x, mouse_y):
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        stats.score_screen_active = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bunkers):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if not stats.score_screen_active:
        if button_clicked and not stats.game_active:
            ai_settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            if play_button.rect.collidepoint(mouse_x, mouse_y):
                stats.reset_stats()
                stats.game_active = True
                ai_settings.start_game_timer()
                sb.prep_score()
                sb.prep_high_score()
                sb.prep_level()
                sb.prep_ships()
                aliens.empty()
                bullets.empty()
                create_fleet(ai_settings, screen, aliens)
                create_bunkers(bunkers=bunkers, screen=screen)
                ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, explosions, ufos, score_button,
                  back_button, lasers, bunkers):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # Draw pixels
    bunkers.draw(screen)
    aliens.draw(screen)
    explosions.draw(screen)
    ufos.draw(screen)
    for laser in lasers.sprites():
        laser.draw_laser()
    bullets.draw(screen)
    sb.show_score()
    if stats.score_screen_active:
        draw_high_score_screen(ai_settings=ai_settings, screen=screen, back_button=back_button)
    if not stats.game_active and not stats.score_screen_active:
        draw_main_screen(ai_settings, screen, play_button, score_button)
    pygame.display.flip()


def update_lasers(lasers):
    lasers.update()


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets, explosions, ufos, bunkers):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, stats, sb, aliens, bullets, explosions)
    check_ufo_bullet_collision(ufos=ufos, bullets=bullets, stats=stats, sb=sb)
    check_bunker_bullet_collision(bullets=bullets, bunkers=bunkers)


def check_bunker_bullet_collision(bullets, bunkers):
    if pygame.sprite.groupcollide(bunkers, bullets, False, True):
        pass


def check_bullet_alien_collision(ai_settings, screen, stats, sb, aliens, bullets, explosions):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    alien_points = 0
    if collisions:
        for alien in collisions:
            # Create new explosion
            explosion = Explosion(screen=screen, x=alien.rect.x, y=alien.rect.y, ai_settings=ai_settings)
            explosions.add(explosion)
            alien_points += ai_settings.alien_points[alien.alien_type]
            # Check if alien can shoot, if true, check for closest alien above it to grant it shooting ability
            if alien.can_shoot:
                inline = []
                column = alien.column_number
                height = 0
                for next_shooter in aliens:
                    if next_shooter.column_number == column:
                        inline.append(next_shooter)
                        if next_shooter.rect.y > height:
                            height = next_shooter.rect.y
                if inline:
                    for target in inline:
                        if target.rect.y == height:
                            target.can_shoot = True
                            break

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
    collision = pygame.sprite.groupcollide(ufos, bullets, True, True)
    ufo_value = 0
    if collision:
        for ufo in collision:
            ufo.destroy_ufo()
            ufo_value = ufo.point_value
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


def update_aliens(ai_settings, stats, screen, sb, aliens, ship, bullets, lasers):
    check_fleet_edges(ai_settings, aliens)
    aliens.update(lasers)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    if stats.ships_left > 1:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        # Game is Over
        # Read High Scores
        game_score = stats.score
        with open('scores.json') as file:
            scores = json.load(file)

        for score in scores['scores']:
            if game_score > score['score']:
                stats.input_name_active = True
                while stats.input_name_active:
                    display_enter_name_box(ai_settings=ai_settings, screen=screen, stats=stats)
                    score['score'] = game_score
                    score['name'] = stats.player_name.upper()
                    with open('scores.json', 'w') as outfile:
                        json.dump(scores, outfile, indent=4)
                break

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


def draw_main_screen(ai_settings, screen, play_button, score_button):
    screen.fill((0, 0, 0))
    # Title
    title_font = pygame.font.SysFont(None, 135, bold=True)
    title_text = title_font.render("SPACE", 1, (255, 255, 255))
    title_rect = title_text.get_rect()
    title_rect.center = ai_settings.screen_width / 2, 100
    screen.blit(title_text, title_rect)

    title2_font = pygame.font.SysFont(None, 82, bold=True)
    title2_text = title2_font.render("INVADERS", 1, (50, 255, 50))
    title2_rect = title2_text.get_rect()
    title2_rect.center = ai_settings.screen_width / 2, 175
    screen.blit(title2_text, title2_rect)

    # Alien Images
    alien1 = pygame.image.load('images/alien1a.png')
    alien1 = pygame.transform.scale(alien1, (48, 32))
    alien1_rect = alien1.get_rect()
    alien1_rect.topleft = (ai_settings.screen_width / 2 - 24 - 100, 300)

    alien2 = pygame.image.load('images/alien2a.png')
    alien2 = pygame.transform.scale(alien2, (44, 32))
    alien2_rect = alien2.get_rect()
    alien2_rect.topleft = (ai_settings.screen_width / 2 - 22 - 100, 375)

    alien3 = pygame.image.load('images/alien3a.png')
    alien3 = pygame.transform.scale(alien3, (32, 32))
    alien3_rect = alien3.get_rect()
    alien3_rect.topleft = (ai_settings.screen_width / 2 - 16 - 100, 450)

    ufo = pygame.image.load('images/mothership.png')
    ufo = pygame.transform.scale(ufo, (64, 28))
    ufo_rect = ufo.get_rect()
    ufo_rect.topleft = (ai_settings.screen_width / 2 - 32 - 100, 525)

    scores_font = pygame.font.SysFont(None, 48)
    score1_text = scores_font.render("= 10 PTS", 1, (255, 255, 255))
    score1_rect = score1_text.get_rect()
    score1_rect.topleft = (ai_settings.screen_width / 2 - 50, 300)
    screen.blit(score1_text, score1_rect)

    score2_text = scores_font.render("= 20 PTS", 1, (255, 255, 255))
    score2_rect = score2_text.get_rect()
    score2_rect.topleft = (ai_settings.screen_width / 2 - 50, 375)
    screen.blit(score2_text, score2_rect)

    score3_text = scores_font.render("= 40 PTS", 1, (255, 255, 255))
    score3_rect = score3_text.get_rect()
    score3_rect.topleft = (ai_settings.screen_width / 2 - 50, 450)
    screen.blit(score3_text, score3_rect)

    ufo_text = scores_font.render("= ??? PTS", 1, (255, 255, 255))
    ufo_text_rect = ufo_text.get_rect()
    ufo_text_rect.topleft = (ai_settings.screen_width / 2 - 50, 525)
    screen.blit(ufo_text, ufo_text_rect)

    screen.blit(alien1, alien1_rect)
    screen.blit(alien2, alien2_rect)
    screen.blit(alien3, alien3_rect)
    screen.blit(ufo, ufo_rect)
    score_button.draw_button()
    play_button.draw_button()


def draw_high_score_screen(ai_settings, screen, back_button):
    screen.fill((0, 0, 0))
    back_button.draw_button()

    # Title
    title_font = pygame.font.SysFont(None, 82, bold=True)
    title_text = title_font.render("High Scores", 1, (230, 55, 55))
    title_rect = title_text.get_rect()
    title_rect.center = ai_settings.screen_width / 2, 100
    screen.blit(title_text, title_rect)

    # Read scores file
    with open('scores.json') as file:
        scores = json.load(file)

    # Scores
    scores_font = pygame.font.SysFont('Consolas', 48)
    offset = 0
    for score in scores['scores']:
        place_text = scores_font.render("{}".format(offset + 1), 1, (111, 217, 122))
        place_rect = place_text.get_rect()
        place_rect.topright = ai_settings.screen_width / 2 - 200, 200 + offset * 50
        screen.blit(place_text, place_rect)

        score_text = scores_font.render("{}".format(score['score']), 1, (247, 217, 132))
        score_rect = score_text.get_rect()
        score_rect.topleft = ai_settings.screen_width / 2 + 50, 200 + offset * 50
        screen.blit(score_text, score_rect)

        name_text = scores_font.render("{}".format(score['name']), 1, (247, 217, 132))
        name_rect = name_text.get_rect()
        name_rect.topleft = ai_settings.screen_width / 2 + 175, 200 + offset * 50
        screen.blit(name_text, name_rect)
        offset += 1


def display_enter_name_box(ai_settings, screen, stats):
    screen.fill((0, 0, 0))

    # Text
    enter_font = pygame.font.SysFont(None, 48)
    enter_name_text = enter_font.render("Enter your Name (3 Letters)", 1, (255, 255, 255))
    enter_name_rect = enter_name_text.get_rect()
    enter_name_rect.center = (ai_settings.screen_width/2, 100)
    screen.blit(enter_name_text, enter_name_rect)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                stats.input_name_active = False
            elif event.key == pygame.K_BACKSPACE:
                stats.player_name = stats.player_name[:-1]
            elif len(stats.player_name) < 3:
                stats.player_name += event.unicode

    # Input Box
    input_box = enter_font.render(stats.player_name.upper(), 1, (255, 255, 255))
    input_rect = input_box.get_rect()
    input_rect.center = (ai_settings.screen_width/2, 200)
    screen.blit(input_box, input_rect)

    pygame.display.update()
