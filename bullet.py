import pygame

class Bullet:
    def __init__(self, x, y, direction, speed, settings, is_monster=False):
        """Initialize the bullet."""
        if is_monster:
            if direction == -1:
                self.image = pygame.image.load("images/Monsters/monsterBullet/MBULLET(right).gif")
            else:
                self.image = pygame.image.load("images/Monsters/monsterBullet/MBULLET(left).gif")

            self.image = pygame.transform.scale(self.image, (settings.monster_bullet_width, settings.monster_bullet_height))
            self.damage = 2.5  # Monster bullet damage
        else:
            self.image = pygame.image.load("images/Bullets/firedBullet (2).png")
            self.image = pygame.transform.scale(self.image, (settings.bullet_width, settings.bullet_height))
            self.bullet_count = settings.max_bullets  # Set max bullets, this can be adjustable
            self.reload_sound = pygame.mixer.Sound("sounds/gun_reload.wav")  # Load reload sound
            self.bow_image = pygame.image.load(settings.bullet_bow_image)
            self.bow_image = pygame.transform.scale(self.bow_image, (settings.bullet_bow_width, settings.bullet_bow_height))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # direction is expected to be -1 for left and 1 for right
        self.speed = speed

        # Flip the bullet image when moving left
        if self.direction == -1 and not is_monster:
            self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally

    def update(self):
        """Update the position of the bullet."""
        self.rect.x += self.direction * self.speed

    def draw(self, screen):
        """Draw the bullet on the screen."""
        screen.blit(self.image, self.rect)

    def draw_bullet_bow(self, screen, settings):
        """Draw the bullet bow to show remaining bullets (for hero only)."""
        if hasattr(self, 'bow_image'):
            for i in range(self.bullet_count):  # Display only the remaining bullets
                offset = i * (settings.bullet_bow_width + 5)  # Add spacing between bullets
                x = settings.bullet_bow_position[0] - offset
                y = settings.bullet_bow_position[1]
                screen.blit(self.bow_image, (x, y))

    def reload(self):
        """Play reload sound and reset the bullet count (for hero only)."""
        if hasattr(self, 'bullet_count'):
            self.bullet_count = 10  # Reset bullet count (adjust if needed)

    def check_collision(self, targets):
        """Check if the bullet collides with any target."""
        for target in targets[:]:
            if self.rect.colliderect(target.rect):  # Check if the bullet collides with the target
                if hasattr(self, 'damage') and self.damage:  # If bullet is from monster
                    target.health -= self.damage  # Apply damage to the player
                targets.remove(target)  # Remove the target on collision only if bullet is from hero
                return True  # Collision detected
        return False