import pygame
from pygame.sprite import Sprite


class Terrain(Sprite):
    """A class to manage the ground."""

    def __init__(self, r_game, terrain_type):
        """Initialize the block and set its starting position"""
        super(Terrain, self).__init__()
        self.screen = r_game.screen
        self.screen_rect = r_game.screen.get_rect()
        self.settings = r_game.settings

        # Load the terrain and get its rect.
        terrain1 = 'images/terrain1.bmp'
        terrain2 = 'images/terrain2.bmp'
        terrain3 = 'images/terrain3.bmp'
        terrain4 = 'images/terrain4.bmp'
        terrain5 = 'images/terrain5.bmp'
        if terrain_type == 1:
            self.terrain = terrain1
        if terrain_type == 2:
            self.terrain = terrain2
        if terrain_type == 3:
            self.terrain = terrain3
        if terrain_type == 4:
            self.terrain = terrain4
        if terrain_type == 5:
            self.terrain = terrain5
        self.image = pygame.image.load(self.terrain)
        self.rect = self.image.get_rect()

        # Start the terrain bottom  of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

class Pad(Sprite):
    """A class to manage the ground."""

    def __init__(self, r_game):
        """Initialize the block and set its starting position"""
        super(Pad, self).__init__()
        self.screen = r_game.screen
        self.screen_rect = r_game.screen.get_rect()
        self.settings = r_game.settings

        # Load the terrain and get its rect.
        self.image = pygame.image.load('images/pad.bmp')
        self.rect = self.image.get_rect()

        # Start the terrain bottom  of the screen.
        self.rect.midbottom = self.screen_rect.midbottom