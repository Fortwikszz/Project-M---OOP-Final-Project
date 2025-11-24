import pygame
from settings import *
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('test', 'Rock2.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)