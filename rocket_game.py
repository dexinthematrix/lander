import sys
from time import sleep
import pygame
from random import randint

from settings import Settings
from game_stats import GameStats
from rocket import Rocket
from terrain import Terrain, Pad
from scoreboard import Scoreboard
from flames import Flames
from button import Button, Banner, InfoButton


class RocketGame:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_bottom = self.screen.get_rect().bottom
        self.bg_color = self.settings.bg_color
        pygame.display.set_caption("Lander")

        # Create and instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.rocket = Rocket(self, 1)
        self.rocket2 = Rocket(self, 2)
        self.rocket2.rect.top = self.screen_bottom
        self.flames = Flames(self)
        self.terrain_group = pygame.sprite.Group()
        self._create_terrain_group()
        self.pad = Pad(self)

        # Make the Play button
        self.play_button = Button(self, "Start", 500, 500)

        # Make the info button
        self.info_button = InfoButton(self, "Instructions", 500, 600)

        # Set the high score file
        self.filename = "highscore.txt"

        # Make a banner of instructions
        self.banner = Banner(self, "Click on 'Start' or press 's'", 350, 100)
        self.banner2 = Banner(self, "Press 'q' to Quit", 350, 200)
        self.show_instructions = Banner(self,"Use up arrow for thrust and left/right arrows to rotate.", 300,650)
        self.show_instructions2 = Banner(self, "Land on the platform with parameters green.  "
                                               "Bonus points for fuel remaining", 300, 700)
        self.info_displayed = False
        # Make a bonus points banner
        bonus_points_str =   "place holder"
        self.banner3 = Banner(self, bonus_points_str, 500, 200)

        # Get sound file:
        self.explosion_sound = pygame.mixer.Sound("explosion.wav")
        self.thrust_sound = pygame.mixer.Sound("thrusters.wav")
        self.applause_sound = pygame.mixer.Sound("applause.wav")
        self.alert_sound = pygame.mixer.Sound("alert.wav")

        pygame.mixer.music.load('lander.wav')
        pygame.mixer.music.set_volume(1.0)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.rocket.update()
                self.flames.update(self.rocket.x, self.rocket.y, self.settings.angle)
                self.settings.height = int(self.settings.screen_height - self.rocket.y - 84)  # 84 is the pad height
                self._check_fuel()
                self.sb.prep_fuel_remaining()
                self.sb.prep_height()
                self.sb.prep_vel_x()
                self.sb.prep_vel_y()
                self.sb.prep_angle()
                self._landed_or_crashed()

            self._update_screen()
            pygame.display.flip()

    def _landed_or_crashed(self):
        """Routine to see whether landed or crashed"""

        self._landing()
        if self.settings.crashed:
            self._crashed()
        elif self.settings.landed:
            self._landed()

    def _landing(self):
        """Routine to check if landing and take appropriate action"""
        contact = pygame.sprite.spritecollideany(self.rocket, self.terrain_group)
        if contact and (self.settings.rocket_vel_y < self.settings.rocket_vel_y_safe)\
                or contact and (self.settings.angle > self.settings.rocket_angle_safe) \
                or contact and (self.settings.angle < -self.settings.rocket_angle_safe) \
                or contact and ((self.settings.rocket_vel_x < -self.settings.rocket_vel_x_safe)
                                or (self.settings.rocket_vel_x > self.settings.rocket_vel_x_safe))\
                or contact and (self.rocket.x > (self.pad.x + 30)
                                or (self.rocket.x < (self.pad.x - 30))) \
                or self.settings.height < -10:
            self.settings.rocket_vel_y = 0
            self.settings.crashed = True
        elif contact and self.settings.rocket_vel_y >= self.settings.rocket_vel_y_safe:
            self.settings.rocket_vel_y = 0
            print(self.settings.rocket_vel_y)
            self.settings.landed = True
        else:
            self.settings.landed = False
            self.settings.crashed = False

    def _landed(self):
        """Routine to add points, print a logo and reset the next ship"""
        self._applause()       # Play explosion sound
        if self.settings.fuel > 10:
            self.settings.bonus_points = self.settings.fuel * 2
        self.stats.score += self.settings.landing_points + int(self.settings.bonus_points)
        self.settings.landings += 1
        self.sb.prep_level()
        self.sb.prep_score()
        self.sb.check_high_score()
        self._bonus_points()
        self._update_screen()
        if self.stats.rockets_left > -1:   # If you land you want to continue!
            # Dont decrement ships left and update scoreboard
            self.sb.prep_rockets()
            self.rocket.restart_rocket()
            self.settings.initialize_dynamic_settings()
            # Get rid of any remaining terrain.
            self.terrain_group.empty()

            # Create a new landscape.

            self._create_terrain_group()

            # Pause
            sleep(1.5)
            # Play soundtrack.
            pygame.mixer.music.unpause()
        else:
            self.stats.game_active = False
            pygame.mixer.music.stop()  # Stop the music playing
            pygame.mouse.set_visible(True)

    def _crashed(self):
        #
        self.rocket2.rect.center = self.rocket.rect.center
        self._explosion()       # Play explosion sound
        self._update_screen()
        sleep(1.5)
        if self.stats.rockets_left > 0:
            # Decrement ships left and update scoreboard
            self.stats.rockets_left -= 1
            self.sb.prep_rockets()

            self.rocket.restart_rocket()
            self.settings.initialize_dynamic_settings()
            self.rocket2.rect.top = self.screen_bottom
            # Get rid of any remaining terrain.
            self.terrain_group.empty()

            # Create a new landscape.
            self._create_terrain_group()

            # Pause
            sleep(1.5)
            # Play soundtrack.
            pygame.mixer.music.unpause()
        else:
            self.stats.game_active = False
            pygame.mixer.music.stop()  # Stop the music playing
            pygame.mouse.set_visible(True)

    def _check_events(self):
        """ Watch for keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open(self.filename, 'w') as file_object:
                    highscore = str(self.stats.high_score)
                    print(highscore)
                    file_object.write(highscore)
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_info_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game if player clicks Start"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.landings = 0
            self.settings.initialize_dynamic_settings()
            self.settings.fuel = self.settings.fuel_capacity
            self.rocket2.rect.top = self.screen_bottom
            self.stats.reset_stats()
            self.sb.prep_images()
            self.stats.game_active = True

            # Get rid of any remaining bugs and bullets.
            self.terrain_group.empty()

            # Create a new fleet and center the ship.
            self._create_terrain_group()
            self.rocket.restart_rocket()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Play soundtrack.
            pygame.mixer.music.play(-1)

    def _check_info_button(self, mouse_pos):
        """Show instructions if the player clicks for instructions"""
        info_button_clicked = self.info_button.rect.collidepoint(mouse_pos)
        if info_button_clicked and not self.stats.game_active and not self.info_displayed:
            self.info_displayed = True
        elif info_button_clicked and not self.stats.game_active and self.info_displayed:
            self.info_displayed = False
        #elif info_button_clicked and not self.stats.game_active and self.info_displayed:
            #self.show_instructions.
    def _check_s(self, check_s):
        """Start a new game if player clicks 's' to start"""
        if check_s and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.landings = 0
            self.settings.initialize_dynamic_settings()
            self.settings.fuel = self.settings.fuel_capacity
            self.rocket2.rect.top = self.screen_bottom
            self.stats.reset_stats()
            self.sb.prep_images()
            self.stats.game_active = True

            # Get rid of the old terrain
            self.terrain_group.empty()

            # Create a new fleet and center the ship.
            self._create_terrain_group()
            self.rocket.restart_rocket()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)
            # Play soundtrack.
            pygame.mixer.music.play(-1)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # set moving right flag true.
            self.rocket.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Set moving left flag true.
            self.rocket.moving_left = True
        elif event.key == pygame.K_UP:
            # set moving up flag true.
            if self.settings.fuel > 0:
                self.rocket.thrust_applied = True
                self._thrust()  # Thrust sound
        elif event.key == pygame.K_s:
            check_s = True
            self._check_s(check_s)
        elif event.key == pygame.K_q:
            with open(self.filename, 'w') as file_object:
                highscore = str(self.stats.high_score)
                print(highscore)
                file_object.write(highscore)
            sys.exit()


    def _check_keyup_events(self, event):
        """"Respond to releases"""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = False
        if event.key == pygame.K_UP:
            self.rocket.thrust_applied = False
            pygame.mixer.Sound.stop(self.thrust_sound)

    def _check_fuel(self):
        if self.settings.fuel < 200:
            self._alert()  # Play alert sound

    def _thrust(self):
        # Pause the music, allow shot noise, unpause the music.
        pygame.mixer.Sound.set_volume(self.thrust_sound, 1.0)
        pygame.mixer.Sound.play(self.thrust_sound)

    def _explosion(self):
        # Pause any music, allow the explosion then unpause any music.
        pygame.mixer.music.pause()
        pygame.mixer.Sound.stop(self.alert_sound)
        pygame.mixer.Sound.play(self.explosion_sound)
        pygame.mixer.Sound.stop(self.alert_sound)

    def _applause(self):
        # Pause any music, allow the 'yeah' then unpause any music.
        pygame.mixer.music.pause()
        pygame.mixer.Sound.stop(self.alert_sound)
        pygame.mixer.Sound.play(self.applause_sound)

    def _alert(self):
        # Pause any music, allow the explosion then unpause any music.
        pygame.mixer.Sound.set_volume(self.alert_sound, 0.1)
        pygame.mixer.Sound.play(self.alert_sound)

    def _bonus_points(self):
        bonus = int(self.settings.bonus_points)
        bonus_points_str = f"You got {str(bonus)} fuel bonus points."
        self.banner3.update_banner(bonus_points_str)

    def _create_terrain_group(self):
        """Create the terrain group made up of terrain blocks"""
        # Create a terrain block.
        terrain = Terrain(self, 1)
        terrain_width, terrain_height = terrain.rect.size
        available_space_x = self.settings.screen_width
        number_of_terrain_blocks = available_space_x // (terrain_width - 2)
        pad_number = randint(2, number_of_terrain_blocks - 2)
        for terrain_number in range(number_of_terrain_blocks):
            if terrain_number == pad_number:
                self._create_pad(terrain_number)
            else:
                terrain_type = randint(1, 5)
                self._create_terrain(terrain_number, terrain_type)

    def _create_terrain(self, terrain_number, terrain_type):
        """Create a terrain block """
        terrain = Terrain(self, terrain_type)
        terrain_width, terrain_height = terrain.rect.size
        terrain.x = (terrain_width - 2) * terrain_number
        terrain.rect.x = terrain.x
        terrain.rect.y = 750
        self.terrain_group.add(terrain)

    def _create_pad(self, terrain_number):
        """Create a pad block """
        self.pad = Pad(self)
        pad_width, pad_height = self.pad.rect.size
        self.pad.x = (pad_width - 2) * terrain_number
        self.pad.rect.x = self.pad.x
        self.pad.rect.y = 750
        self.terrain_group.add(self.pad)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.bg_color)
        self.rocket.blitme()
        self.rocket2.blitme()
        self.flames.blitme()
        self.terrain_group.draw(self.screen)
        if self.settings.bonus_points > 0:
            self.banner3.draw_button()
            sleep(1.5)
        # Draw the score information
        self.sb.show_score()

        # Draw the Start button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.info_button.draw_button()
            self.banner.draw_button()
            self.banner2.draw_button()
            if self.info_displayed:
                self.show_instructions.draw_button()
                self.show_instructions2.draw_button()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run game.
    r = RocketGame()
    r.run_game()
