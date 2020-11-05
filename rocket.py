import pygame
from pygame.sprite import Sprite
import math


class Rocket(Sprite):
    """A class to manage the rocket."""

    def __init__(self, r_game, lander_pic):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = r_game.screen
        self.screen_rect = r_game.screen.get_rect()
        self.settings = r_game.settings

        ship_normal = 'images/ship2.bmp'
        ship_explode = 'images/ship2_explode2.bmp'
        if lander_pic == 1:
            self.lander = ship_normal
        elif lander_pic == 2:
            self.lander = ship_explode
        # Load the rocket image and get its rect.
        self.image0 = pygame.image.load(self.lander)
        self.image = self.image0
        self.rect = self.image.get_rect()

        # Start the rocket int the middle of the screen.
        self.rect.center = self.screen_rect.center

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.thrust_applied = False

    def update(self):
        """Update the rocket's position based on the movement flag"""
        # Update the ship's x and y values, not the rect.
        # Rotation of the ship alters the direction of the thrust and therefore x and y
        if self.moving_right and self.settings.angle > -self.settings.angle_limit:
            self.settings.angle -= 0.3
        if self.moving_left and self.settings.angle < self.settings.angle_limit:
            self.settings.angle += 0.3
        # Apply thrust if 'thrust-applied' is set.
        if self.thrust_applied:
            self.settings.rocket_vel_y += (self.settings.thrust * math.cos(self.settings.angle * math.pi / 180))\
                                            + self.settings.g
            self.settings.rocket_vel_x -= (self.settings.thrust * math.sin(self.settings.angle * math.pi / 180))
            self.settings.fuel -= self.settings.fuel_burn
        else:
            self.settings.rocket_vel_y += self.settings.g

        self.y -= self.settings.rocket_vel_y
        self.x += self.settings.rocket_vel_x

        self.image = pygame.transform.rotozoom(self.image0, self.settings.angle, 1)
        # Update rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the rocket at its current location"""
        self.screen.blit(self.image, self.rect)

    def restart_rocket(self):
        """Redraw the rocket on screen"""
        self.rect.midtop = self.screen_rect.midtop
        self.y = self.rect.y
        self.x = self.rect.x
