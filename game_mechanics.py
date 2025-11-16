import pygame
import sys

class GameMechanics:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Load the start button image and set its position
        self.button_image = pygame.image.load("images/Startbutton.png")
        self.button_rect = self.button_image.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height - 50))

        # Load and scale the game mechanics background image
        self.game_mechanics_image = pygame.image.load("images/Game_mechanics.png")
        self.game_mechanics_image = pygame.transform.scale(
            self.game_mechanics_image, (self.settings.screen_width, self.settings.screen_height)
        )

    def draw(self):
        """Draw the game mechanics screen."""
        self.screen.blit(self.game_mechanics_image, (0, 0))  # Draw the game mechanics background
        self.screen.blit(self.button_image, self.button_rect)  # Draw the start button

    def check_button_click(self, event):
        """Check if the start button is clicked."""
        if self.button_rect.collidepoint(event.pos):  # If the click is inside the button's area
            return True
        return False

    def show_until_start(self):
        """Display the game mechanics screen until the start button is clicked."""
        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.check_button_click(event):  # Check if the start button was clicked
                        waiting_for_start = False
                        break

            self.draw()  # Draw the game mechanics screen
            pygame.display.flip()
            pygame.time.Clock().tick(30)  # Control the frame rate
