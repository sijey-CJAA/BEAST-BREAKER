import pygame
from PIL import Image
from bullet import Bullet  # Import the Bullet class

class Monster:
    def __init__(self, x, y, side, image_path, settings):
        self.x = x
        self.y = y
        self.side = side
        self.image_path = image_path
        self.settings = settings
        self.speed = settings.monster_speed

        # Load and resize images
        self.images = self.load_gif_frames(image_path)
        self.current_frame_index = 0
        self.rect = self.images[0].get_rect(topleft=(self.x, self.y))

        if "Monster1" in image_path:
            self.health = 2
        elif "Monster2" in image_path:
            self.health = 8
        elif "Monster3" in image_path:
            self.health = 5
        elif "Monster4" in image_path:
            self.health = 10

        self.facing_left = side == "right"
        self.last_attack_time = 0  # Timer to manage continuous damage
        self.last_bullet_time = 0  # Timer to manage bullet firing
        self.bullets = []  # List to store bullets fired by the monster

    def load_gif_frames(self, gif_path):
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = gif.copy().convert("RGBA")
                if "Monster1(running).gif" in gif_path or "Monster1.1(running).gif" in gif_path:
                    frame = frame.resize((100, 100))
                elif "Monster3(running).gif" in gif_path or "Monster3.1(running).gif" in gif_path:
                    frame = frame.resize((150, 150))
                frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def update(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = (dx**2 + dy**2)**0.5

        # Avoid division by zero
        if distance != 0:
            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Constrain the monster's vertical movement within the player's boundaries
        if self.rect.top < self.settings.min_y:
            self.rect.top = self.settings.min_y
        if self.rect.bottom > self.settings.max_y:
            self.rect.bottom = self.settings.max_y

        self.current_frame_index = (self.current_frame_index + 1) % len(self.images)

        # Flip the images based on the direction towards the player
        if dx > 0 and self.facing_left:
            self.images = [pygame.transform.flip(img, True, False) for img in self.images]
            self.facing_left = False
        elif dx < 0 and not self.facing_left:
            self.images = [pygame.transform.flip(img, True, False) for img in self.images]
            self.facing_left = True

        # Fire bullets every 10 seconds
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time > 10000:  # 10000 milliseconds = 10 seconds
            self.fire_bullet()
            self.last_bullet_time = current_time

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.x < 0 or bullet.rect.x > self.settings.screen_width:
                self.bullets.remove(bullet)

    def fire_bullet(self):
        direction = -1 if self.facing_left else 1
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction, speed=self.settings.monster_bullet_speed, settings=self.settings, is_monster=True)
        self.bullets.append(bullet)
        self.settings.monster_fire_sound.play()  # Play the monster fire sound

    def is_firing(self):
        """Return whether the monster is currently firing a bullet."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_bullet_time < 100  # Example: Firing considered for 100ms after firing

    def reached_player(self, player):
        return self.rect.colliderect(player.rect)

    def attack_player(self, player, health_bar, continuous_damage_sound):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > 1000:  # Apply damage every 1 second
            player.health -= 1  # Apply continuous damage to the player
            health_bar.take_damage(1)  # Update the health bar
            continuous_damage_sound.play()  # Play the continuous damage sound
            self.last_attack_time = current_time

    def draw(self, screen):
        screen.blit(self.images[self.current_frame_index], self.rect)
        self.draw_health_bar(screen)
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_health_bar(self, screen):
        health_bar_width = self.rect.width
        health_bar_height = 5
        health_percentage = self.health / self.get_max_health()
        health_bar_fill = health_bar_width * health_percentage

        health_bar_rect = pygame.Rect(self.rect.left, self.rect.top - health_bar_height - 2, health_bar_width, health_bar_height)
        health_bar_fill_rect = pygame.Rect(self.rect.left, self.rect.top - health_bar_height - 2, health_bar_fill, health_bar_height)

        pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), health_bar_fill_rect)

    def get_max_health(self):
        if "Monster1" in self.image_path:
            return 2
        elif "Monster2" in self.image_path:
            return 8
        elif "Monster3" in self.image_path:
            return 5
        elif "Monster4" in self.image_path:
            return 10
        return 1

    def take_damage(self, amount):
        self.health -= amount
        self.settings.monster_hit_sound.play()  # Play the monster hit sound
        if self.health <= 0:
            self.health = 0  # Ensure health does not go below zero