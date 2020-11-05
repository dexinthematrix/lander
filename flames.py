import pygame
from pygame.sprite import Sprite
import math


class Flames(Sprite):
    """A class to manage the flames."""

    def __init__(self, r_game):
        """Initialize the block and set its starting position"""
        super(Flames, self).__init__()
        self.screen = r_game.screen
        self.screen_rect = r_game.screen.get_rect()
        self.settings = r_game.settings
        self.rocket = r_game.rocket
        self.thrust_applied = r_game.rocket.thrust_applied

        # Load the terrain and get its rect.
        self.image1 = pygame.image.load('images/flame1.bmp')
        self.image = self.image1
        self.flame_rect = self.image.get_rect()

        # Start the terrain bottom  of the screen.
        self.flame_rect.midtop = self.rocket.rect.midbottom

    def update(self, x, y, angle):
        """Update the flames"""
        # Rotate the image by the angle first then apply the components of x and y as offset from the lander
        if self.rocket.thrust_applied:
            self.image = pygame.transform.rotozoom(self.image1, angle, 1)
            self.flame_rect.x = x  + 8 + (29 * math.sin(angle * math.pi / 180))
            self.flame_rect.y = y + 5 + (32 * math.cos(angle * math.pi / 180))
        else:
            self.flame_rect.midtop = self.screen_rect.midbottom



    def blitme(self):
        """Draw the rocket at its current location"""
        self.screen.blit(self.image, self.flame_rect)
