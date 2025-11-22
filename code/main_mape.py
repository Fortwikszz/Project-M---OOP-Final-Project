import pygame

class Level:
    def __init__(self):
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.vissible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        
    def run(self):
        # Update and draw the game level
        pass
