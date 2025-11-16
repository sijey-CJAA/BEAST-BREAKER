import pygame

class Button:
    def __init__(self, image_path, pos, action=None):
        """Initialize button attributes."""
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=pos)
        self.action = action

    def draw(self, screen):
        """Draw the button on the screen."""
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        """Check if the button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False