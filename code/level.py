import pygame
from settings import *
from tiled import Tile
from player import Player

class Level:
    def __init__(self):
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # sprite setup
        self.create_map()
        
    def create_map(self):
        # Create the game map 
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites])
        
    def run(self):
        boundary_rect = self.display_surface.get_rect()
        self.visible_sprites.update(boundary_rect) 
        self.visible_sprites.draw(self.display_surface)

        if hasattr(self, 'player'):
            self.player.debug_draw(self.display_surface)