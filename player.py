import pygame
from PIL import Image

class Player:
    def __init__(self, settings, selected_hero, game, level=1):
        self.settings = settings
        self.selected_hero = selected_hero
        self.state = "idle"  # Default state
        self.facing_left = False  # Default facing direction
        self.game = game  # Reference to the main game instance

        # Initialize health
        self.health = 100  # Set the initial health value

        # Load all frames for each state
        self.idle_frames = self.load_and_resize_gif(
            self.settings.hero_gifs[self.selected_hero]["idle"],
            settings.player_width, settings.player_height
        )
        self.running_frames = self.load_and_resize_gif(
            self.settings.hero_gifs[self.selected_hero]["running"],
            settings.player_width, settings.player_height
        )
        self.shooting_frames = self.load_and_resize_gif(
            self.settings.hero_gifs[self.selected_hero]["shooting"],
            settings.player_width, settings.player_height
        )

        # Animation properties
        self.current_frames = self.idle_frames
        self.current_frame_index = 0
        self.last_animation_update = pygame.time.get_ticks()
        self.animation_interval = 10  # Milliseconds per frame

        # Default to the first frame of idle
        self.current_image = self.idle_frames[0]

        # Center the player on the screen
        self.x = self.settings.screen_width // 2 - self.current_image.get_width() // 2
        self.y = self.settings.screen_height // 2 - self.current_image.get_height() // 2

        # Create the rect object based on player position and size
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # Player speed
        self.settings.update_player_speed(level)
        self.speed = self.settings.player_speed

    def load_and_resize_gif(self, gif_path, target_width, target_height):
        """Load and resize all frames of a GIF."""
        gif = Image.open(gif_path)
        frames = []

        try:
            while True:
                frame = gif.copy().convert("RGBA")
                frame = frame.resize((target_width, target_height))
                frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(frames))
        except EOFError:
            pass  # End of GIF

        return frames

    def update_animation(self):
        """Update the current animation frame based on the timer."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update > self.animation_interval:
            self.last_animation_update = current_time
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_frames)
            self.current_image = self.current_frames[self.current_frame_index]

        # Update rect dimensions and position to match the current frame
        self.rect.size = self.current_image.get_size()
        self.rect.topleft = (self.x, self.y)

    def update(self, keys):
        """Update the player's state and position based on input."""
        self.state = "idle"  # Reset to idle unless movement is detected

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.state = "running"
            self.facing_left = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.state = "running"
            self.facing_left = False

        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.state = "running"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.state = "running"

        # Shooting
        if keys[pygame.K_SPACE]:
            self.state = "shooting"

        # Clamp player position within boundaries
        self.x = max(self.settings.min_x, min(self.x, self.settings.max_x - self.current_image.get_width()))
        self.y = max(self.settings.min_y, min(self.y, self.settings.max_y - self.current_image.get_height()))

        # Update the player's rect based on the updated x, y position
        self.rect.topleft = (self.x, self.y)

        # Update the current frames based on the state
        if self.state == "idle":
            self.current_frames = self.idle_frames
        elif self.state == "running":
            self.current_frames = self.running_frames
        elif self.state == "shooting":
            self.current_frames = self.shooting_frames

        # Update the animation
        self.update_animation()

    def draw(self, screen):
        """Draw the player on the screen."""
        # Flip the image if facing left
        image_to_draw = pygame.transform.flip(self.current_image, self.facing_left, False)
        screen.blit(image_to_draw, self.rect.topleft)

    @property
    def dimensions(self):
        """Get the current player's dimensions (width and height)."""
        return self.current_image.get_width(), self.current_image.get_height()

    def take_damage(self, damage):
        """Reduce the player's health by the specified damage amount."""
        self.health -= damage
        if self.health < 0:
            self.health = 0