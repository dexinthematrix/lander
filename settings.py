import math


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialise the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)

        # Rocket settings
        self.rocket_limit = 3
        self.g = -0.002          # Used in rocket_game
        self.thrust = 0.003     # Used in rocket_game
        self.fuel_capacity = 500
        self.rocket_vel_x_safe = 0.1
        self.rocket_vel_y_safe = -0.5
        self.rocket_angle_safe = 5
        self.fuel_burn = 0.1
        self.angle_limit = 80.0
        self.height = self.screen_height
        # Points for a safe landing
        self.landing_points = 500
        self.landings = 0
        # Rate of level difficulty increase
        self.difficulty_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.fuel = self.fuel_capacity
        self.rocket_vel_x = 0.2 * math.pow(self.difficulty_scale, self.landings)
        self.rocket_vel_y = 0.2 * math.pow(self.difficulty_scale, self.landings)
        self.angle = 10.0 * math.pow(self.difficulty_scale, self.landings)
        self.bonus_points = 0
        self.landed = False
        self.crashed = False
