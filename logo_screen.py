import pygame
import sys
import cv2
import numpy as np

class LogoScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.sound_effect = pygame.mixer.Sound("sounds/INTRO.wav")

    def play_logo_video(self):
        """Play the game logo video using OpenCV and Pygame."""
        # Open the video file using OpenCV
        cap = cv2.VideoCapture(self.settings.logo_video_path)
        self.sound_effect.play()
        
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return

        # Get the video FPS (frames per second)
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Get the original video dimensions
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Calculate the target width and height for landscape orientation
        target_width = self.screen.get_width()
        target_height = int(target_width * original_height / original_width)

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            # Resize the frame to fit the screen, keeping the aspect ratio
            frame_resized = cv2.resize(frame, (target_width, target_height))

            # Convert the frame from BGR (OpenCV format) to RGB (Pygame format)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Create a Pygame surface from the frame
            frame_surface = pygame.surfarray.make_surface(frame_rgb)

            # Rotate the frame if needed
            frame_surface = pygame.transform.rotate(frame_surface, self.settings.logo_rotation_angle)

            # Get the coordinates from settings
            x, y = self.settings.logo_position

            # Blit the video frame to the screen at the desired position
            self.screen.blit(frame_surface, (x, y))
            pygame.display.update()

            # Delay to match the FPS of the video
            pygame.time.wait(int(500 / fps))

            # Event handling to close the game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        cap.release()  # Release the video capture object
