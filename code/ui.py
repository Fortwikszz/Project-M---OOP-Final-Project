import pygame
from code.settings import *

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)

    def draw_health_bar(self):
        bar_width = self.player.max_health * 2
        bar_height = 20
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.display_surface, (100, 100, 100), (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.display_surface, (230, 30, 30), (20, 20, bar_width * health_ratio, bar_height))

    def draw_stamina_bar(self):
        bar_width = self.player.max_stamina * 2
        bar_height = 20
        stamina_ratio = self.player.stamina / self.player.max_stamina
        pygame.draw.rect(self.display_surface, (100, 100, 100), (20, 50, bar_width, bar_height))
        pygame.draw.rect(self.display_surface, (0, 255, 50), (20, 50, bar_width * stamina_ratio, bar_height))

    def display(self):
        self.draw_health_bar()
        self.draw_stamina_bar()