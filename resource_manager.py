# resource_manager.py
import pygame

class ResourceManager:
    def __init__(self, settings):
        self.settings = settings
        self.images = {}
        self.sounds = {}
        self.load_resources()

    def load_resources(self):
        self.load_images()
        self.load_sounds()

    def load_images(self):
        self.images['bullet_bow'] = self.load_image(self.settings.bullet_bow_image, self.settings.bullet_bow_width, self.settings.bullet_bow_height)
        self.images['menu_button'] = self.load_image("images/buttons/menu_button.png", self.settings.menu_button_width, self.settings.menu_button_height)
        self.images['resume_button'] = self.load_image("images/buttons/resume_button.png")
        self.images['new_game_button'] = self.load_image("images/buttons/new_game.png")
        self.images['quit_button'] = self.load_image("images/buttons/quit_button.png")
        self.load_wave_images()

    def load_wave_images(self):
        for level in range(1, 6):
            for wave in range(1, 5):
                key = f"l{level}w{wave}"
                image_path = f"images/waves/{key}.png"
                self.images[key] = pygame.image.load(image_path)

    def load_sounds(self):
        self.sounds['gunshot'] = self.load_sound("sounds/gun_shot.wav")
        self.sounds['gun_empty'] = self.load_sound("sounds/gun_empty.wav")
        self.sounds['game_over'] = self.load_sound("sounds/new_sounds/game_over_sound.mp3")
        self.sounds['start_button'] = self.load_sound("sounds/new_sounds/start_button-to-game.mp3")
        self.sounds['monster_roar'] = self.load_sound("sounds/new_sounds/monster_roar.wav")
        self.sounds['selection'] = self.load_sound("sounds/new_sounds/selection_sound.mp3")
        self.sounds['player_hit'] = self.load_sound("sounds/new_sounds/player_hit1.wav")
        self.sounds['monster_hit'] = self.load_sound("sounds/new_sounds/monster_hit1.wav")
        self.sounds['monster_fire'] = self.load_sound("sounds/new_sounds/monster_fire.wav")
        self.sounds['continuous_damage'] = self.load_sound("sounds/new_sounds/continuous_damage.wav")

    def load_image(self, path, width=None, height=None):
        image = pygame.image.load(path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image

    def load_sound(self, path):
        return pygame.mixer.Sound(path)