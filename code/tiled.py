import pygame
from code.settings import *
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image=None):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-40, -100)