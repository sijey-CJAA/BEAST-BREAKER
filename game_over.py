import pygame
import sys
from button import Button  # Import the Button class

class GameOver:
    def __init__(self, ai_game):
        """Initialize game over screen attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ai_game = ai_game  # Reference to the main game instance

        # Load the game over image and resize it to fit the screen
        self.game_over_image = pygame.image.load('images/GameOver/gameover.jpg')
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.screen_rect.width, self.screen_rect.height))
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.topleft = (0, 0)

        # Create buttons
        self.play_again_button = Button('images/GameOver/playagain.png', (self.ai_game.settings.play_again_button_x, self.ai_game.settings.play_again_button_y), self.play_again)
        self.exit_button = Button('images/GameOver/exit.png', (self.ai_game.settings.exit_button_x, self.ai_game.settings.exit_button_y), self.exit_game)

        # Load the "Special Elite" font for displaying total monsters killed
        self.font = pygame.font.Font('fonts/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf', 48)
    
    def draw_game_over(self):
        """Draw the game over screen."""
        self.screen.blit(self.game_over_image, self.game_over_rect)
        self.play_again_button.draw(self.screen)
        self.exit_button.draw(self.screen)

        # Display total monsters killed
        total_killed_text = f"{self.ai_game.total_monsters_killed}"
        total_killed_image = self.font.render(total_killed_text, True, (255, 255, 255))
        total_killed_rect = total_killed_image.get_rect()
        total_killed_rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 60)
        self.screen.blit(total_killed_image, total_killed_rect)

    def play_again(self):
        """Restart the game to character selection phase."""
        self.ai_game.reset_to_character_selection()

    def exit_game(self):
        """Exit the game."""
        pygame.quit()
        sys.exit()

    def check_events(self, event):
        """Check for button clicks."""
        if self.play_again_button.is_clicked(event):
            self.play_again()
        elif self.exit_button.is_clicked(event):
            self.exit_game()