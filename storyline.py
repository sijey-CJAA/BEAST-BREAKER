import pygame
import sys
from PIL import Image

class Storyline:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.story_images = [
            "images/storyline/1png.png", 
            "images/storyline/2png.png", 
            "images/storyline/3png.png", 
            "images/storyline/4png.png", 
            "images/storyline/5png.png"
        ]
        self.current_index = 0
        self.skip_button_rect = pygame.Rect(10, 10, 100, 40)  # Skip button area
        self.next_button_rect = pygame.Rect(10, 60, 100, 40)  # Next button area

        # Load all frames for each story GIF
        self.story_frames = [self.load_gif_frames(image, (self.screen.get_width(), self.screen.get_height())) for image in self.story_images]
        self.current_frame = 0
        self.frame_delay = 1  # Adjust delay for animation speed
        self.frame_counter = 0

        # Load and configure background music
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/BACKSTORY.mp3")  # Load the MP3 file

    def load_gif_frames(self, gif_path, target_size):
        """Load frames from a GIF file."""
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = gif.copy().convert("RGBA")
                frame = frame.resize(target_size)
                frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def draw_buttons(self):
        """Draw skip and next buttons on the screen."""
        # Draw skip button
        pygame.draw.rect(self.screen, (200, 0, 0), self.skip_button_rect)  # Red button
        skip_text = pygame.font.Font(None, 30).render("SKIP", True, (255, 255, 255))
        self.screen.blit(skip_text, (20, 15))

        # Draw next button
        pygame.draw.rect(self.screen, (0, 200, 0), self.next_button_rect)  # Green button
        next_text = pygame.font.Font(None, 30).render("NEXT", True, (255, 255, 255))
        self.screen.blit(next_text, (20, 65))

    def handle_buttons(self, event):
        """Handle button clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
            mouse_pos = event.pos
            if self.skip_button_rect.collidepoint(mouse_pos):  # Skip button clicked
                return "skip"
            if self.next_button_rect.collidepoint(mouse_pos):  # Next button clicked
                self.current_index += 1
                self.current_frame = 0  # Reset frame index for new GIF
                if self.current_index >= len(self.story_images):  # End of storyline
                    return "end"
        return None

    def play_storyline(self):
        """Play the storyline phase."""
        # Play the background music infinitely
        pygame.mixer.music.play(loops=-1)  # -1 means infinite loop

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Handle button interactions
                action = self.handle_buttons(event)
                if action == "skip":
                    pygame.mixer.music.stop()  # Stop the music
                    return  # Skip the storyline phase
                if action == "end":
                    pygame.mixer.music.stop()  # Stop the music
                    return  # Proceed to the next phase

            # Draw the current GIF frame
            frames = self.story_frames[self.current_index]
            self.screen.fill((0, 0, 0))  # Clear screen with black background
            self.screen.blit(frames[self.current_frame], (0, 0))

            # Update frame for animation
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.frame_counter = 0

            # Draw buttons
            self.draw_buttons()

            pygame.display.flip()
            pygame.time.Clock().tick(100)  # Adjust FPS
