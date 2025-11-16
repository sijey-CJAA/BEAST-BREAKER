import pygame
import sys

class CharacterSelection:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.bg_image_path = 'images/CHARACTER_SELECTION1.png'

        # Load the background image and resize it to full screen
        self.bg_image = pygame.image.load(self.bg_image_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))

        # Load and resize button images
        self.button1 = pygame.image.load('images/button1.png')
        self.button1 = pygame.transform.scale(self.button1, (self.settings.button_width, self.settings.button_height))
        self.button2 = pygame.image.load('images/button2.png')
        self.button2 = pygame.transform.scale(self.button2, (self.settings.button_width, self.settings.button_height))

        # Button positions (defined in settings)
        self.button1_rect = self.button1.get_rect(topleft=(self.settings.button1_x, self.settings.button1_y))
        self.button2_rect = self.button2.get_rect(topleft=(self.settings.button2_x, self.settings.button2_y))

    def run_character_selection(self):
        """Run the character selection screen."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Check if the player clicked on Button 1 (Hero1)
                    if self.button1_rect.collidepoint(mouse_x, mouse_y):
                        return 'Hero1'
                    # Check if the player clicked on Button 2 (Hero2)
                    elif self.button2_rect.collidepoint(mouse_x, mouse_y):
                        return 'Hero2'

            # Clear the screen at the start of each loop
            self.screen.fill((0, 0, 0))

            # Draw background image (resized to full screen)
            self.screen.blit(self.bg_image, (0, 0))

            # Draw buttons
            self.screen.blit(self.button1, self.button1_rect.topleft)
            self.screen.blit(self.button2, self.button2_rect.topleft)

            pygame.display.flip()
