import pygame
import sys
from settings import Settings
from logo_screen import LogoScreen
from storyline import Storyline
from character_selection import CharacterSelection
from player import Player
from game_mechanics import GameMechanics
from bullet import Bullet
from overall_wave import OverallWave
from health_bar import HealthBar
from game_over import GameOver
from start import Start  # Import the Start class
from resource_manager import ResourceManager  # Import the ResourceManager class
from PIL import Image
import itertools

class BeastBreaker:
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Set up fullscreen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width, self.settings.screen_height = self.screen.get_size()
        pygame.display.set_caption("BEAST BREAKER")

        # Initialize audio
        pygame.mixer.init()

        # Initialize resource manager
        self.resources = ResourceManager(self.settings)

        # Load background music for the main game loop
        self.main_game_music = "sounds/GAME_BG.mp3"
        self.music_volume = 0.50  # Set default volume (50%)
        pygame.mixer.music.set_volume(self.music_volume)

        # Initialize storyline and logo screen
        self.logo_screen = LogoScreen(self.screen, self.settings)
        self.storyline = Storyline(self.screen, self.settings)

        # Initialize placeholders for player and other objects
        self.player = None
        self.shooting_cooldown = 0
        self.bullets = []
        self.bullet_count = 10
        self.max_bullets = 10
        self.space_pressed = False  # Flag to track space bar state

        # Bullet bow image
        self.bullet_bow_image = self.resources.images['bullet_bow']
        self.bullet_bow_rect = self.bullet_bow_image.get_rect()
        self.bullet_bow_rect.topright = self.settings.bullet_bow_position

        # Background GIF frames
        self.gif_frames = self.load_gif_frames(
            self.settings.bg_image_path,
            (self.settings.screen_width, self.settings.screen_height),
        )
        self.current_frame_index = 0

        # Initialize the health bar
        self.health_bar = HealthBar(self.screen, self.settings)

        # Initialize wave system (will be set after player is selected)
        self.overall_wave = None

        # Initialize game over screen
        self.total_monsters_killed = 0  # Track total monsters killed
        self.game_over_screen = GameOver(self)  # Create the GameOver instance

        # Load wave images
        self.wave_images = self.resources.images
        self.show_wave_image = False
        self.wave_image = None

        # Load menu button image
        self.menu_button_image = self.resources.images['menu_button']
        self.menu_button_rect = self.menu_button_image.get_rect(
            topleft=(self.settings.menu_button_x, self.settings.menu_button_y))

        # Load menu box and buttons images
        self.resume_button_image = self.resources.images['resume_button']
        self.new_game_button_image = self.resources.images['new_game_button']
        self.quit_button_image = self.resources.images['quit_button']

        # Initialize pause state
        self.paused = False

    def load_gif_frames(self, gif_path, target_size):
        """Load and return all frames from a GIF resized to the target size."""
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = gif.copy().convert("RGBA")
                frame = frame.resize(target_size)
                frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(frames))
        except EOFError:
            pass  # End of GIF
        return frames

    def handle_events(self):
        """Handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_events(event)

    def handle_keydown_events(self, event):
        """Handle keydown events."""
        if event.key == pygame.K_ESCAPE:
            self.quit_game()

    def handle_mouse_events(self, event):
        """Handle mouse button down events."""
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_button_rect.collidepoint(mouse_pos):
            self.show_menu()
        self.game_over_screen.check_events(event)

    def quit_game(self):
        """Quit the game."""
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    def handle_input(self):
        """Handle player movement, shooting, and reloading."""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Shooting
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1

        if keys[pygame.K_SPACE]:
            if not self.space_pressed and self.shooting_cooldown == 0:
                self.space_pressed = True
                if self.bullet_count > 0:
                    self.player.state = "shooting"
                    self.shooting_cooldown = 10  # Shooting cooldown
                    self.shoot_bullet()
                    self.bullet_count -= 1
                else:
                    self.resources.sounds['gun_empty'].play()
        else:
            self.space_pressed = False

        # Reloading
        if keys[pygame.K_r] and self.bullet_count < self.max_bullets:
            self.reload_bullets()

    def shoot_bullet(self):
        """Create a bullet and add it to the bullets list."""
        bullet_x = self.player.x + self.settings.player_width // 2
        bullet_y = self.player.y + self.settings.player_height // 2
        direction = -1 if self.player.facing_left else 1
        bullet = Bullet(
            bullet_x, bullet_y, direction, self.settings.bullet_speed, self.settings
        )
        self.bullets.append(bullet)
        self.resources.sounds['gunshot'].play()

    def reload_bullets(self):
        """Reload bullets to maximum capacity."""
        self.bullet_count = self.max_bullets
        reload_sound = pygame.mixer.Sound("sounds/gun_reload.wav")
        reload_sound.play()

    def update_bullets(self):
        """Update the position of bullets and remove off-screen bullets."""
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.x < 0 or bullet.rect.x > self.settings.screen_width:
                self.bullets.remove(bullet)

    def draw_bullet_bow(self):
        """Draw the bullet bow to show remaining bullets."""
        for i in range(self.bullet_count):
            offset = i * (self.bullet_bow_rect.width + 5)
            self.screen.blit(
                self.bullet_bow_image, (self.bullet_bow_rect.x - offset, self.bullet_bow_rect.y)
            )

    def run_game(self):
        """Main game loop."""
        # Run the start screen
        self.run_start_screen()

        # Play logo screen and storyline
        self.logo_screen.play_logo_video()
        self.storyline.play_storyline()

        # Run character selection
        self.run_character_selection()

        # Show game mechanics
        self.show_game_mechanics()

        # Start the main game loop
        self.main_game_loop()

    def run_start_screen(self):
        """Run the start screen."""
        start_screen = Start(self.screen, self.settings)
        
        # Load and play the start screen music
        start_music = "sounds/new_sounds/start_music.mp3"
        pygame.mixer.music.load(start_music)
        pygame.mixer.music.play(-1)  # Play the start music in a loop

        start_screen.run_start_screen()

        # Stop the start screen music once the start screen is done
        pygame.mixer.music.stop()

    def main_game_loop(self):
        """The main game loop."""
        # Initialize wave system
        self.overall_wave = OverallWave(self.screen, self.settings, self.resources.sounds['player_hit'], self.resources.sounds['monster_hit'], self.resources.sounds['monster_fire'], self.resources.sounds['continuous_damage'])
        self.overall_wave.start_wave()
        # Play monster roar sound at the start of the game
        self.resources.sounds['monster_roar'].play()

        # Initialize bullets list
        self.bullets = []  # List of bullets

        # Play main game music
        pygame.mixer.music.load(self.main_game_music)
        pygame.mixer.music.play(-1)

        for level in range(1, 6):
            for wave in range(1, 5):
                print(f"Wave {wave} starting in Level {level}...")
                key = f"l{level}w{wave}"
                self.wave_image = self.wave_images.get(key)

                if self.wave_image:
                    self.show_wave_image = True
                    self.screen.blit(self.wave_image, (self.settings.screen_width // 2 - self.wave_image.get_width() // 2, 10))
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Display the image for 2 seconds
                else:
                    print(f"Image not found for {key}")

                self.resources.sounds['monster_roar'].play()

                while True:
                    self.handle_events()
                    if not self.paused:
                        # Update monsters and pass both player and bullets
                        self.overall_wave.update_monsters(self.player, self.bullets, self.health_bar)

                        # Handle input
                        self.handle_input()

                        # Update bullets
                        self.update_bullets()

                        # Check wave completion status
                        wave_status = self.overall_wave.check_wave_completion()

                        # Check if the player's health is zero or below
                        if self.player.health <= 0:
                            print("Game Over!")
                            pygame.mixer.music.stop()
                            self.show_game_over_screen()
                            return  # Exit the main game loop to allow restarting

                        if wave_status == "game_over":
                            print("Game Over!")
                            pygame.mixer.music.stop()
                            self.show_game_over_screen()
                            return  # Exit the main game loop to allow restarting

                        elif wave_status == "next_wave":
                            break  # Exit the inner while loop to progress to the next wave

                    # Draw background, player, and objects
                    self.screen.blit(self.gif_frames[self.current_frame_index], (0, 0))
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.gif_frames)

                    # Draw player
                    self.player.draw(self.screen)

                    # Draw bullets
                    for bullet in self.bullets:
                        bullet.draw(self.screen)

                    # Draw bullet bow
                    self.draw_bullet_bow()

                    # Draw health bar
                    self.health_bar.draw()

                    # Draw monsters
                    self.overall_wave.draw_monsters()

                    # Draw menu button
                    self.screen.blit(self.menu_button_image, self.menu_button_rect)

                    pygame.display.flip()
                    self.clock.tick(30)

        print("Congratulations! You've completed all levels!")
        pygame.mixer.music.stop()
        self.show_game_over_screen()

    def show_menu(self):
        """Show the menu with resume, new game, and quit buttons."""
        menu_running = True
        # Calculate dimensions and positions for the menu box and buttons
        menu_width, menu_height = 400, 300
        menu_x = (self.settings.screen_width - menu_width) // 2
        menu_y = (self.settings.screen_height - menu_height) // 2

        resume_button_rect = self.resume_button_image.get_rect(center=(self.settings.screen_width // 2, menu_y + 70))
        new_game_button_rect = self.new_game_button_image.get_rect(center=(self.settings.screen_width // 2, menu_y + 170))
        quit_button_rect = self.quit_button_image.get_rect(center=(self.settings.screen_width // 2, menu_y + 250))

        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if resume_button_rect.collidepoint(mouse_pos):
                        menu_running = False  # Resume the game
                        self.paused = False
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()  # Exit the main game
                    elif new_game_button_rect.collidepoint(mouse_pos):
                        menu_running = False
                        self.reset_to_character_selection()  # Direct to character selection phase

            self.screen.fill((0, 0, 0))  # Fill the screen with black
            pygame.draw.rect(self.screen, (200, 200, 200), (menu_x, menu_y, menu_width, menu_height))  # Draw menu box
            self.screen.blit(self.resume_button_image, resume_button_rect)
            self.screen.blit(self.new_game_button_image, new_game_button_rect)
            self.screen.blit(self.quit_button_image, quit_button_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def run_character_selection(self):
        """Run the character selection phase."""
        character_selection = CharacterSelection(self.screen, self.settings)
        selected_hero = character_selection.run_character_selection()

        # Play selection sound when a button is clicked
        self.resources.sounds['selection'].play()

        # Create the player with the selected hero and pass the game instance
        self.player = Player(self.settings, selected_hero, self)

        # Update player settings and position
        self.settings.player_width, self.settings.player_height = self.player.dimensions
        self.player.x = self.settings.screen_width // 2 - self.player.current_image.get_width() // 2
        self.player.y = self.settings.screen_height // 2 - self.player.current_image.get_height() // 2

    def show_game_mechanics(self):
        """Show the game mechanics screen."""
        game_mechanics = GameMechanics(self.screen, self.settings)
        game_mechanics.show_until_start()

        # Play the start button sound when the button is pressed
        self.resources.sounds['start_button'].play()

    def show_game_over_screen(self):
        """Display the game over screen and handle button interactions."""
        self.resources.sounds['game_over'].play()  # Play the game-over sound
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # Check for button clicks on the game over screen
                self.game_over_screen.check_events(event)

            self.screen.fill(self.settings.bg_color)
            self.game_over_screen.draw_game_over()
            pygame.display.flip()

    def reset_to_character_selection(self):
        """Reset the game state to the character selection phase."""
        self.total_monsters_killed = 0  # Reset the total monsters killed
        self.health_bar.reset_health()  # Reset the health bar
        self.run_character_selection()
        self.show_game_mechanics()
        self.main_game_loop()

if __name__ == "__main__":
    ai = BeastBreaker()
    ai.run_game()