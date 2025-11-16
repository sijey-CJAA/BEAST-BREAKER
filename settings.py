import pygame

class Settings:
    def __init__(self):
        """Initialize game settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)  # Black background
        self.bg_image_path = "images/BG.gif"  # Background image

        # Character Selection Button Positions
        self.button1_x = 300  # X-coordinate for Hero1 button
        self.button1_y = 400  # Y-coordinate for Hero1 button
        self.button2_x = 500  # X-coordinate for Hero2 button
        self.button2_y = 400  # Y-coordinate for Hero2 button

        # Player settings (default hero is Hero1)
        self.player_width = 50
        self.player_height = 50
        self.base_player_speed = 5  # Base speed for the player
        self.player_speed = self.base_player_speed

        # Define boundaries for player movement
        self.min_x = -10  # Left boundary
        self.max_x = self.screen_width + 500  # Right boundary
        self.min_y = 130  # Top boundary
        self.max_y = self.screen_height + 150  # Bottom boundary

        # Bullet settings
        self.bullet_speed = 20
        self.bullet_width = 25  # Default bullet width
        self.bullet_height = 15  # Default bullet height

        # Monster bullet settings
        self.monster_bullet_speed = 5  # Speed of monster bullets
        self.monster_bullet_width = 50  # Width of monster bullets
        self.monster_bullet_height = 50  # Height of monster bullets

        # Logo screen settings
        self.logo_video_path = "videos/START_FINAL.mp4"  # Path to the logo video
        self.logo_rotation_angle = 90  # Rotation angle in degrees (0 means no rotation)
        self.logo_position = (0, 0)  # X, Y coordinates for the logo video on screen

        # Character Selection Phase Settings
        self.character_selection_bg_path = "images/CHARACTER_SELECTION1.png"  # Background for character selection
        self.hero1_button_path = "images/button1.png"  # Hero 1 button image path
        self.hero2_button_path = "images/button2.png"  # Hero 2 button image path
        
        # Character Selection Button Positions
        self.button1_x = 150  # X-coordinate for Hero1 button
        self.button1_y = 500  # Y-coordinate for Hero1 button
        self.button2_x = 750  # X-coordinate for Hero2 button
        self.button2_y = 500  # Y-coordinate for Hero2 button

        # Button dimensions
        self.button_width = 350
        self.button_height = 250

        # Hero GIF paths
        self.hero_gifs = {
            "Hero1": {
                "idle": "images/Heroes/Hero1(idle).gif",
                "running": "images/Heroes/Hero1(running).gif",
                "shooting": "images/Heroes/Hero1(shooting).gif",
            },
            "Hero2": {
                "idle": "images/Heroes/Hero2(idle).gif",
                "running": "images/Heroes/Hero2(running).gif",
                "shooting": "images/Heroes/Hero2(shooting).gif",
            },
        }

        # Selected hero (default is Hero1, can be overwritten after selection)
        self.selected_hero = "Hero1"

        # Player dimensions adjustments
        self.player_width *= 3  # Adjust size if needed
        self.player_height *= 3

        # Bullet bow settings
        self.bullet_bow_width = 35  # Adjust width of each bullet in bow
        self.bullet_bow_height = 45  # Adjust height of each bullet in bow
        self.bullet_bow_image = "images/Bullets/ammo_rr.png"  # Bullet bow image path
        self.bullet_bow_position = (self.screen_width - 375, 100)  # Position (x, y) of bullet bow on screen
        self.max_bullets = 10  # Maximum bullets per round

        # Health bar settings
        self.max_health = 100  # Maximum hits the player can take
        self.health_bar_width = 400  # Width of the health bar
        self.health_bar_height = 30  # Height of the health bar
        self.health_bar_position = (40, 40)  # Position of the health bar (top-left corner)

        self.monster_speed = 10  # Speed at which monsters move towards the player

        # Monster settings
        self.monster_width = 10
        self.monster_height = 20
        self.monster_speed = 1

        # Game Over Button Positions
        self.play_again_button_x = 200  # X-coordinate for Play Again button
        self.play_again_button_y = 400  # Y-coordinate for Play Again button
        self.exit_button_x = 800  # X-coordinate for Exit button
        self.exit_button_y = 400  # Y-coordinate for Exit button

        # Menu Button Position and Size
        self.menu_button_x = self.screen_width + 190  # X-coordinate for Menu button
        self.menu_button_y = -200  # Y-coordinate for Menu button
        self.menu_button_width = 500  # Width of the Menu button
        self.menu_button_height = 500  # Height of the Menu button

        # Menu Box and Buttons Positions and Sizes
        self.menu_box_width = 150
        self.menu_box_height = 150
        self.menu_resume_button_y = 50  # Y-coordinate for Resume button relative to the menu box
        self.menu_new_game_button_y = 60  # Y-coordinate for New Game button relative to the menu box
        self.menu_quit_button_y = 70  # Y-coordinate for Quit button relative to the menu box

        # Load sounds
        self.load_sounds()

    def load_sounds(self):
        """Load game sounds."""
        self.gunshot_sound = pygame.mixer.Sound("sounds/gun_shot.wav")
        self.gun_empty_sound = pygame.mixer.Sound("sounds/gun_empty.wav")
        self.game_over_sound = pygame.mixer.Sound("sounds/new_sounds/game_over_sound.mp3")
        self.start_button_sound = pygame.mixer.Sound("sounds/new_sounds/start_button-to-game.mp3")
        self.monster_roar_sound = pygame.mixer.Sound("sounds/new_sounds/monster_roar.wav")
        self.selection_sound = pygame.mixer.Sound("sounds/new_sounds/selection_sound.mp3")
        self.player_hit_sound = pygame.mixer.Sound("sounds/new_sounds/player_hit1.wav")
        self.monster_hit_sound = pygame.mixer.Sound("sounds/new_sounds/monster_hit1.wav")
        self.monster_fire_sound = pygame.mixer.Sound("sounds/new_sounds/monster_fire.wav")

    def update_player_speed(self, level):
        """Update the player's speed based on the current level."""
        self.player_speed = self.base_player_speed + 2 * (level - 1)