import pygame
from code.settings import *
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image=None, hitbox=None):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        if hitbox:
            self.hitbox = self.rect.inflate(-hitbox[0], -hitbox[1])
        else:
            self.hitbox = self.rect