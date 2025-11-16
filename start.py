import pygame
import sys
from PIL import Image

class Start:
    def __init__(self, screen, settings):
        """Initialize the start screen with background GIF and buttons."""
        self.screen = screen
        self.settings = settings

        # Load the background GIF and extract frames
        self.gif = Image.open('images/1BG.gif')
        self.frames = []
        try:
            while True:
                self.frames.append(self.gif.copy())
                self.gif.seek(len(self.frames))
        except EOFError:
            pass  # End of gif

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Milliseconds per frame

        # Resize frames to fit the screen
        self.frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert() for frame in self.frames]
        self.frames = [pygame.transform.scale(frame, (self.settings.screen_width, self.settings.screen_height)) for frame in self.frames]

        # Load buttons
        self.start_button_image = pygame.image.load("images/start.png").convert_alpha()
        self.exit_button_image = pygame.image.load("images/quit.png").convert_alpha()

        # Define button sizes
        self.button_width = 200
        self.button_height = 80

        # Resize button images
        self.start_button_image = pygame.transform.scale(self.start_button_image, (self.button_width, self.button_height))
        self.exit_button_image = pygame.transform.scale(self.exit_button_image, (self.button_width, self.button_height))

        # Set button positions
        self.start_button_rect = self.start_button_image.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height - 150))
        self.exit_button_rect = self.exit_button_image.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height - 50))

    def draw(self):
        """Draw the start screen with background GIF and buttons."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.screen.blit(self.frames[self.current_frame], (0, 0))  # Draw the background GIF
        self.screen.blit(self.start_button_image, self.start_button_rect)  # Draw the start button
        self.screen.blit(self.exit_button_image, self.exit_button_rect)  # Draw the exit button

    def check_button_click(self, event):
        """Check if any button is clicked."""
        if self.start_button_rect.collidepoint(event.pos):  # If the start button is clicked
            return 'start'
        elif self.exit_button_rect.collidepoint(event.pos):  # If the exit button is clicked
            return 'exit'
        return None

    def run_start_screen(self):
        """Display the start screen until a button is clicked."""
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = self.check_button_click(event)
                    if action == 'start':  # Proceed to the logo screen sequence
                        waiting_for_click = False
                        break
                    elif action == 'exit':  # Exit the game
                        pygame.quit()
                        sys.exit()

            self.draw()  # Draw the start screen
            pygame.display.flip()
            pygame.time.Clock().tick(30)  # Control the frame rate