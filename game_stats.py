
class GameStats:
    """Track statistics for rocket_game"""

    def __init__(self, r_game):
        self.settings = r_game.settings
        self.reset_stats()
        # Start Rocket Game in an inactive state.
        self.game_active = False

        # High score should not be reset
        with open("highscore.txt") as file_object:
            self.high_score = int(file_object.read())

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.rockets_left = self.settings.rocket_limit
        self.score = 0
        self.fuel_remaining = self.settings.fuel
