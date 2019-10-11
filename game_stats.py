class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        self.score_screen_active = False
        self.input_name_active = False
        self.ships_left = None
        self.score = None
        self.level = None
        self.high_score = 0
        self.player_name = ""
        self.reset_stats()

    def reset_stats(self):
        self.player_name = ""
        self.score = 0
        self.level = 1
        self.ships_left = self.ai_settings.ship_limit
