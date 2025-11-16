import pygame

class HealthBar:
    def __init__(self, screen, settings):
        """Initialize the health bar."""
        self.screen = screen
        self.settings = settings
        self.max_health = settings.max_health
        self.current_health = settings.max_health

        # Health bar dimensions and position
        self.width = settings.health_bar_width
        self.height = settings.health_bar_height
        self.position = settings.health_bar_position

        # Colors
        self.border_color = (255, 255, 255)  # White border
        self.health_color = (0, 255, 0)  # Green health
        self.bg_color = (255, 0, 0)  # Red background for lost health

    def take_damage(self, amount):
        """Reduce the health by the given amount."""
        self.current_health = max(0, self.current_health - amount)

    def reset_health(self):
        """Reset health to the maximum."""
        self.current_health = self.max_health

    def draw(self):
        """Draw the health bar on the screen."""
        # Calculate the health bar fill width
        fill_width = (self.current_health / self.max_health) * self.width

        # Draw the background (lost health)
        pygame.draw.rect(self.screen, self.bg_color, (*self.position, self.width, self.height))

        # Draw the current health
        pygame.draw.rect(self.screen, self.health_color, (*self.position, fill_width, self.height))

        # Draw the border
        pygame.draw.rect(self.screen, self.border_color, (*self.position, self.width, self.height), 2)
