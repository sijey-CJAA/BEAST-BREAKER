import pygame
import random
from monster import Monster  # Ensure the Monster class is correctly implemented and imported

class OverallWave:
    def __init__(self, screen, settings, player_hit_sound, monster_hit_sound, monster_fire_sound, continuous_damage_sound):
        self.screen = screen
        self.settings = settings
        self.current_wave = 1
        self.current_level = 1
        self.max_waves = 4
        self.max_levels = 5  # Increased to 5 levels
        self.monsters = []  # List to store all active monsters
        self.monster_images = {
            1: [("images/Monsters/Monster1.1(running).gif", 5)],
            2: [("images/Monsters/Monster2(running).gif", 1)],
            3: [("images/Monsters/Monster3(running).gif", 6)],  # Updated to have only Monster3
            4: [("images/Monsters/Monster4(running).gif", 1)],
        }
        self.last_update_time = pygame.time.get_ticks()
        self.frame_delay = 50  # Delay in milliseconds between each frame update
        self.player_hit_sound = player_hit_sound  # Store the player hit sound
        self.monster_hit_sound = monster_hit_sound  # Store the monster hit sound
        self.monster_fire_sound = monster_fire_sound  # Store the monster fire sound
        self.continuous_damage_sound = continuous_damage_sound  # Store the continuous damage sound

    def start_wave(self):
        """Start a new wave by spawning monsters."""
        if self.current_wave in self.monster_images:
            wave_monsters = self.monster_images[self.current_wave]
            for monster_image, count in wave_monsters:
                count += self.current_level - 1  # Add additional monsters based on the current level
                for _ in range(count):
                    # Determine spawn location based on a random choice between left and right
                    side = random.choice(["left", "right"])
                    if side == "left":
                        x = -self.settings.monster_width  # Just off the left side of the screen
                    else:
                        x = self.settings.screen_width  # Just off the right side of the screen

                    # Random vertical position within the player's boundaries
                    y = random.randint(self.settings.min_y, self.settings.max_y - self.settings.monster_height)

                    # Spawn all monsters simultaneously
                    monster = Monster(x, y, side, monster_image, self.settings)
                    
                    # Increase monster speed based on the current level
                    monster.speed += .5 * (self.current_level - 1)
                    
                    # Flip the monster image if it spawns from the right side
                    if side == "right":
                        monster.images = [pygame.transform.flip(img, True, False) for img in monster.images]

                    self.monsters.append(monster)

    def update_monsters(self, player, bullets, health_bar):
        """Update monster positions and handle interactions with the player and health bar."""
        monsters_to_remove = []  # List to track monsters to remove
        current_time = pygame.time.get_ticks()

        if current_time - self.last_update_time > self.frame_delay:
            for monster in self.monsters:
                monster.update(player)  # Ensure monsters update with player position in mind

                # Check if monster is hit by any bullet
                for bullet in bullets[:]:  # Use a copy of the list to avoid modifying it while iterating
                    if bullet.rect.colliderect(monster.rect):  # Check for collision
                        bullets.remove(bullet)  # Remove the bullet upon hit
                        monster.health -= 1  # Decrease monster health
                        self.monster_hit_sound.play()  # Play the monster hit sound
                        if monster.health <= 0:
                            monsters_to_remove.append(monster)  # Mark monster for removal
                            player.game.total_monsters_killed += 1  # Update the total monsters killed
                        break  # Stop checking other bullets for this monster

                # Check if monster reached player
                if monster.reached_player(player):
                    monster.attack_player(player, health_bar, self.continuous_damage_sound)  # Apply continuous damage to the player

                # Handle bullets fired by monsters
                for monster_bullet in monster.bullets[:]:  # Use a copy of the list to avoid modifying it while iterating
                    if monster_bullet.rect.colliderect(player.rect):
                        player.health -= monster_bullet.damage
                        health_bar.take_damage(monster_bullet.damage)
                        self.player_hit_sound.play()  # Play the player hit sound
                        if monster_bullet in monster.bullets:
                            monster.bullets.remove(monster_bullet)

                    # Check for collision between player's bullets and monster's bullets
                    for bullet in bullets[:]:  # Use a copy of the list to avoid modifying it while iterating
                        if bullet.rect.colliderect(monster_bullet.rect):
                            if bullet in bullets:
                                bullets.remove(bullet)
                            if monster_bullet in monster.bullets:
                                monster.bullets.remove(monster_bullet)
                            break  # Exit the inner loop since the bullet has been removed

                # Play monster fire sound whenever a monster fires a bullet
                if monster.is_firing():
                    self.monster_fire_sound.play()

            self.last_update_time = current_time  # Update the last update time

        # Remove all marked monsters after the iteration
        for monster in monsters_to_remove:
            if monster in self.monsters:
                self.monsters.remove(monster)
                
    def draw_monsters(self):
        """Draw all monsters on the screen."""
        for monster in self.monsters:
            monster.draw(self.screen)

    def check_wave_completion(self):
        """Check if the wave is complete (all monsters are gone)."""
        if not self.monsters:
            self.current_wave += 1
            if self.current_wave > self.max_waves:
                self.current_wave = 1
                self.current_level += 1
                if self.current_level > self.max_levels:
                    return "game_over"  # All levels completed
            self.start_wave()  # Start the next wave or level
            return "next_wave"
        return None