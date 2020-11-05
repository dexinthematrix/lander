import pygame.font
from pygame.sprite import Group

from rocket import Rocket


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, r_game):
        """Initialize scoreboard attributes"""
        self.r_game = r_game
        self.screen = r_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = r_game.settings
        self.stats = r_game.stats

        # Font settings for scoring information.
        self.text_color = (230, 230, 230)
        self.text_red = (255, 10, 10)
        self.text_green = (10, 255, 10)
        self.font = pygame.font.SysFont(None, 40)

        # Prepare the initial score image.
        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_rockets()
        self.prep_fuel_remaining()
        self.prep_height()
        self.prep_vel_x()
        self.prep_vel_y()
        self.prep_angle()


    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"L {self.settings.landings}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Display the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 5
        self.level_rect.right =  self.score_rect.right

    def prep_rockets(self):
        """Show how many ships are left."""
        self.rockets = Group()
        for rocket_number in range(self.stats.rockets_left):
            rocket = Rocket(self.r_game, 1)
            rocket.rect.x = 10 + (rocket_number * rocket.rect.width)
            rocket.rect.y = 10
            self.rockets.add(rocket)

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score,-1)
        score_str = "Score {:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 5

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top right of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect_top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_fuel_remaining(self):
        """Turn the fuel remaining into a rendered image."""
        fuel_remaining = self.settings.fuel
        fuel_remaining_str = "Fuel {:10.0f}".format(fuel_remaining)
        if fuel_remaining > 200:
            self.fuel_remaining_image = self.font.render(fuel_remaining_str, True,
                                                         self.text_color, self.settings.bg_color)
        else:
            self.fuel_remaining_image = self.font.render(fuel_remaining_str, True,
                                                         self.text_red, self.settings.bg_color)

        self.fuel_remaining_rect = self.fuel_remaining_image.get_rect()
        self.fuel_remaining_rect.left = self.screen_rect.left
        self.fuel_remaining_rect.top = 45
        #Display the fuel remaining to the left or the score.

    def prep_height(self):
        """Turn the height remaining into a rendered image."""
        height = self.settings.height
        height_str = "Height     {:,}".format(height)

        self.height_image = self.font.render(height_str, True, self.text_color, self.settings.bg_color)
        self.height_rect = self.height_image.get_rect()
        self.height_rect.left = self.screen_rect.left
        self.height_rect.top = self.fuel_remaining_rect.bottom + 5
        # Display the fuel height to the left or the fuel.

    def prep_vel_x(self):
        """Turn the velocity x into a rendered image."""
        vel_x = self.settings.rocket_vel_x
        vel_x_str = "Vel x {:10.2f}".format(vel_x)
        if vel_x < - self.settings.rocket_vel_x_safe or vel_x > self.settings.rocket_vel_x_safe:
            self.vel_x_image = self.font.render(vel_x_str, True, self.text_red, self.settings.bg_color)
        else:
            self.vel_x_image = self.font.render(vel_x_str, True, self.text_green, self.settings.bg_color)
        self.vel_x_rect = self.vel_x_image.get_rect()
        self.vel_x_rect.top = self.height_rect.bottom + 5
        self.vel_x_rect.left = self.screen_rect.left


    def prep_vel_y(self):
        """Turn the velocity y into a rendered image."""
        vel_y = self.settings.rocket_vel_y
        vel_y_str = "Vel y {:10.2f}".format(vel_y)
        if vel_y < self.settings.rocket_vel_y_safe or vel_y > 0:
            self.vel_y_image = self.font.render(vel_y_str, True, self.text_red, self.settings.bg_color)
        else:
            self.vel_y_image = self.font.render(vel_y_str, True, self.text_green, self.settings.bg_color)
        self.vel_y_rect = self.vel_y_image.get_rect()
        self.vel_y_rect.top = self.vel_x_rect.bottom + 5
        self.vel_y_rect.left = self.screen_rect.left

    def prep_angle(self):
        """Show the current angle in a rendered image."""
        angle = self.settings.angle
        angle_str = "Angle {:10.2f}".format(angle)
        if angle > self.settings.rocket_angle_safe or angle < -self.settings.rocket_angle_safe:
            self.angle_image = self.font.render(angle_str, True, self.text_red, self.settings.bg_color)
        else:
            self.angle_image = self.font.render(angle_str, True, self.text_green, self.settings.bg_color)
        self.angle_rect = self.angle_image.get_rect()
        self.angle_rect.top = self.vel_y_rect.bottom + 5
        self.angle_rect.left = self.screen_rect.left

    def show_score(self):
        """Draw the scores, level and ships remaining to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.fuel_remaining_image, self.fuel_remaining_rect)
        self.screen.blit(self.height_image, self.height_rect)
        self.screen.blit(self.vel_x_image, self.vel_x_rect)
        self.screen.blit(self.vel_y_image, self.vel_y_rect)
        self.screen.blit(self.angle_image, self.angle_rect)
        self.rockets.draw(self.screen)
