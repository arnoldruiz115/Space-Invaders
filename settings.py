import pygame
import random


class Settings:
    # A class to store all Settings
    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 896
        self.bg_color = (20, 44, 71)
        self.ship_speed_factor = None
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed_factor = None
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (252, 173, 3)
        self.bullets_allowed = 1

        # Alien settings
        self.alien_speed_factor = None
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.laser_speed_factor = None
        self.min_shot_time = None
        self.max_shot_time = None
        self.shot_frequency_factor = 1.5

        # Scoring
        self.alien_points = []

        # Level Settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # Random Event Settings
        self.start_tick = pygame.time.get_ticks()
        self.spawn_time = random.randint(15000, 25000)

    def initialize_dynamic_settings(self):
        self.alien_points = {
            "alien1": 10,
            "alien2": 20,
            "alien3": 40
        }
        self.laser_speed_factor = 4
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 8
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.min_shot_time = 5000
        self.max_shot_time = 15000

    def start_game_timer(self):
        self.start_tick = pygame.time.get_ticks()

    def increase_speed(self):
        if self.min_shot_time != 0:
            self.min_shot_time = int(self.min_shot_time / self.shot_frequency_factor)
            if self.min_shot_time < 0:
                self.min_shot_time = 0
        if self.max_shot_time != 1000:
            self.max_shot_time = int(self.max_shot_time / self.shot_frequency_factor)
            if self.max_shot_time < 1000:
                self.max_shot_time = 1000

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        for i in self.alien_points:
            self.alien_points[i] = int(self.alien_points[i] * self.score_scale)
