import pygame.font


class Button:

    def __init__(self, r_game, msg, x, y):
        self.screen = r_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (255, 10, 10)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Banner:

    def __init__(self, r_game, msg, x, y):
        self.screen = r_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 500, 50
        self.banner_color = (30, 30, 30)
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 35)

        # Build the banner's rect object and center it.
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # The banner message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.banner_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def update_banner(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.banner_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.banner_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class InfoButton:

    def __init__(self, r_game, msg, x, y):
        self.screen = r_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (10, 10, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)