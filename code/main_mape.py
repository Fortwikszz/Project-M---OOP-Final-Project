import pygame
from settings import *
from tiled import Tile
from player import Player

class Level:
    def __init__(self):
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.vissible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # srite setup
        self.create_map()
        
    def create_map(self):
        # Create the game mao
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.vissible_sprites])
                    
    def run(self):
        # Update and draw the game level
        self.vissible_sprites.draw(self.display_surface)
