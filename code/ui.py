import pygame
from code.settings import *
import os

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        
        # Load UI assets
        ui_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "UI")
        try:
            # Load button sprites
            self.button_normal = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Blue.png")).convert_alpha()
            self.button_hover = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Hover.png")).convert_alpha()
            self.button_pressed = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Blue_Pressed.png")).convert_alpha()
            
            # Scale buttons
            button_width = 300
            button_height = 80
            self.button_normal = pygame.transform.scale(self.button_normal, (button_width, button_height))
            self.button_hover = pygame.transform.scale(self.button_hover, (button_width, button_height))
            self.button_pressed = pygame.transform.scale(self.button_pressed, (button_width, button_height))
            self.has_button_sprites = True
        except:
            self.has_button_sprites = False
            print("Warning: Could not load button sprites")
        
        # Menu options
        self.options = ['Start Game', 'Quit']
        self.selected = 0
        self.mouse_over = -1
        
        # Colors
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 215, 0)
        self.text_color = (255, 255, 255)
        
        # Button positions
        self.button_rects = []
        for i in range(len(self.options)):
            rect = pygame.Rect(0, 0, 300, 80)
            rect.center = (WIDTH // 2, HEIGHT // 2 + i * 120)
            self.button_rects.append(rect)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Check mouse hover
        self.mouse_over = -1
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.mouse_over = i
                self.selected = i
                if mouse_clicked:
                    pygame.time.wait(100)
                    return self.selected
        
        # Navigate menu with keyboard
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selected = (self.selected - 1) % len(self.options)
            pygame.time.wait(200)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selected = (self.selected + 1) % len(self.options)
            pygame.time.wait(200)
        
        # Select option with keyboard
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            return self.selected
        
        return None
    
    def display(self):
        # Background
        self.display_surface.fill(self.bg_color)
        
        # Title
        title_text = self.font_large.render('Project M', True, self.title_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.display_surface.blit(title_text, title_rect)
        
        # Menu buttons
        for i, option in enumerate(self.options):
            rect = self.button_rects[i]
            
            # Draw button sprite
            if self.has_button_sprites:
                if i == self.selected:
                    button_img = self.button_hover
                else:
                    button_img = self.button_normal
                self.display_surface.blit(button_img, rect)
            else:
                # Fallback to colored rectangles
                color = (100, 150, 255) if i == self.selected else (60, 60, 100)
                pygame.draw.rect(self.display_surface, color, rect)
                pygame.draw.rect(self.display_surface, (255, 255, 255), rect, 2)
            
            # Draw text
            option_text = self.font_medium.render(option, True, self.text_color)
            text_rect = option_text.get_rect(center=rect.center)
            self.display_surface.blit(option_text, text_rect)
        
        # Instructions
        instructions = self.font_small.render('Use Arrow Keys/WASD, Enter/Space or Click to select', True, (150, 150, 150))
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.display_surface.blit(instructions, instructions_rect)

class PauseMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        
        # Load UI assets
        ui_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "UI")
        try:
            self.button_normal = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Blue.png")).convert_alpha()
            self.button_hover = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Hover.png")).convert_alpha()
            button_width = 300
            button_height = 80
            self.button_normal = pygame.transform.scale(self.button_normal, (button_width, button_height))
            self.button_hover = pygame.transform.scale(self.button_hover, (button_width, button_height))
            self.has_button_sprites = True
        except:
            self.has_button_sprites = False
        
        # Menu options
        self.options = ['Continue', 'Main Menu', 'Quit']
        self.selected = 0
        
        # Colors
        self.title_color = (255, 215, 0)
        self.text_color = (255, 255, 255)
        
        # Button positions
        self.button_rects = []
        for i in range(len(self.options)):
            rect = pygame.Rect(0, 0, 300, 80)
            rect.center = (WIDTH // 2, HEIGHT // 2 - 50 + i * 100)
            self.button_rects.append(rect)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Check mouse hover
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selected = i
                if mouse_clicked:
                    pygame.time.wait(100)
                    return self.selected
        
        # Navigate menu
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selected = (self.selected - 1) % len(self.options)
            pygame.time.wait(200)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selected = (self.selected + 1) % len(self.options)
            pygame.time.wait(200)
        
        # Select option
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            return self.selected
        
        return None
    
    def display(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Title
        title_text = self.font_large.render('PAUSED', True, self.title_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.display_surface.blit(title_text, title_rect)
        
        # Menu buttons
        for i, option in enumerate(self.options):
            rect = self.button_rects[i]
            
            # Draw button sprite
            if self.has_button_sprites:
                button_img = self.button_hover if i == self.selected else self.button_normal
                self.display_surface.blit(button_img, rect)
            else:
                color = (100, 150, 255) if i == self.selected else (60, 60, 100)
                pygame.draw.rect(self.display_surface, color, rect)
                pygame.draw.rect(self.display_surface, (255, 255, 255), rect, 2)
            
            # Draw text
            option_text = self.font_medium.render(option, True, self.text_color)
            text_rect = option_text.get_rect(center=rect.center)
            self.display_surface.blit(option_text, text_rect)
        
        # Instructions
        instructions = self.font_small.render('Press ESC to continue', True, (150, 150, 150))
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.display_surface.blit(instructions, instructions_rect)

class GameOverMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font_large = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        
        # Load UI assets
        ui_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "UI")
        try:
            self.button_normal = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Red.png")).convert_alpha()
            self.button_hover = pygame.image.load(os.path.join(ui_path, "Buttons", "Button_Hover.png")).convert_alpha()
            button_width = 300
            button_height = 80
            self.button_normal = pygame.transform.scale(self.button_normal, (button_width, button_height))
            self.button_hover = pygame.transform.scale(self.button_hover, (button_width, button_height))
            self.has_button_sprites = True
        except:
            self.has_button_sprites = False
        
        # Menu options
        self.options = ['Restart', 'Main Menu', 'Quit']
        self.selected = 0
        
        # Colors
        self.title_color = (220, 20, 60)  # Crimson red
        self.text_color = (255, 255, 255)
        
        # Button positions
        self.button_rects = []
        for i in range(len(self.options)):
            rect = pygame.Rect(0, 0, 300, 80)
            rect.center = (WIDTH // 2, HEIGHT // 2 + 50 + i * 100)
            self.button_rects.append(rect)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        # Check mouse hover
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selected = i
                if mouse_clicked:
                    pygame.time.wait(100)
                    return self.selected
        
        # Navigate menu
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selected = (self.selected - 1) % len(self.options)
            pygame.time.wait(200)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selected = (self.selected + 1) % len(self.options)
            pygame.time.wait(200)
        
        # Select option
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            return self.selected
        
        return None
    
    def display(self):
        # Dark red overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Game Over Title
        title_text = self.font_large.render('GAME OVER', True, self.title_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.display_surface.blit(title_text, title_rect)
        
        # Menu buttons
        for i, option in enumerate(self.options):
            rect = self.button_rects[i]
            
            # Draw button sprite
            if self.has_button_sprites:
                button_img = self.button_hover if i == self.selected else self.button_normal
                self.display_surface.blit(button_img, rect)
            else:
                color = (220, 50, 50) if i == self.selected else (100, 20, 20)
                pygame.draw.rect(self.display_surface, color, rect)
                pygame.draw.rect(self.display_surface, (255, 255, 255), rect, 2)
            
            # Draw text
            option_text = self.font_medium.render(option, True, self.text_color)
            text_rect = option_text.get_rect(center=rect.center)
            self.display_surface.blit(option_text, text_rect)

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.font_large = pygame.font.Font(None, 40)

    def draw_health_bar(self):
        bar_width = self.player.max_health * 2
        bar_height = 20
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.display_surface, (100, 100, 100), (20, 20, bar_width, bar_height))
        pygame.draw.rect(self.display_surface, (230, 30, 30), (20, 20, bar_width * health_ratio, bar_height))
        
        # Health text
        health_text = self.font.render(f'HP: {int(self.player.health)}/{int(self.player.max_health)}', True, (255, 255, 255))
        self.display_surface.blit(health_text, (25, 22))

    def draw_stamina_bar(self):
        bar_width = self.player.max_stamina * 2
        bar_height = 20
        stamina_ratio = self.player.stamina / self.player.max_stamina
        pygame.draw.rect(self.display_surface, (100, 100, 100), (20, 50, bar_width, bar_height))
        pygame.draw.rect(self.display_surface, (0, 255, 50), (20, 50, bar_width * stamina_ratio, bar_height))
        
        # Stamina text
        stamina_text = self.font.render(f'SP: {int(self.player.stamina)}/{int(self.player.max_stamina)}', True, (255, 255, 255))
        self.display_surface.blit(stamina_text, (25, 52))
    
    def draw_level_and_exp(self):
        """Draw level and exp bar in bottom right corner"""
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        
        # Position in bottom right
        panel_width = 250
        panel_height = 80
        panel_x = screen_width - panel_width - 20
        panel_y = screen_height - panel_height - 20
        
        # Background panel
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.display_surface, (40, 40, 60, 200), panel_rect)
        pygame.draw.rect(self.display_surface, (100, 100, 120), panel_rect, 2)
        
        # Level text
        level_text = self.font_large.render(f'Level {self.player.level}', True, (255, 215, 0))
        level_rect = level_text.get_rect(centerx=panel_x + panel_width // 2, top=panel_y + 10)
        self.display_surface.blit(level_text, level_rect)
        
        # EXP bar
        exp_bar_width = panel_width - 40
        exp_bar_height = 20
        exp_bar_x = panel_x + 20
        exp_bar_y = panel_y + 50
        
        exp_ratio = self.player.exp / self.player.exp_to_next_level
        
        # Background bar
        pygame.draw.rect(self.display_surface, (60, 60, 80), 
                        (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height))
        # Progress bar
        pygame.draw.rect(self.display_surface, (100, 200, 255), 
                        (exp_bar_x, exp_bar_y, exp_bar_width * exp_ratio, exp_bar_height))
        # Border
        pygame.draw.rect(self.display_surface, (150, 150, 170), 
                        (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), 2)
        
        # EXP text
        exp_text = self.font.render(f'{int(self.player.exp)}/{int(self.player.exp_to_next_level)} EXP', 
                                     True, (255, 255, 255))
        exp_text_rect = exp_text.get_rect(center=(panel_x + panel_width // 2, exp_bar_y + exp_bar_height // 2))
        self.display_surface.blit(exp_text, exp_text_rect)

    def display_interaction_prompt(self):
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        
        # Position at bottom center
        prompt_text = self.font_large.render('Press E to BOSS', True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height - 100))
        
        # Background box
        bg_rect = prompt_rect.inflate(40, 20)
        pygame.draw.rect(self.display_surface, (40, 40, 60, 230), bg_rect)
        pygame.draw.rect(self.display_surface, (255, 215, 0), bg_rect, 3)
        
        # Draw text
        self.display_surface.blit(prompt_text, prompt_rect)
    
    def draw_boss_health_bar(self, boss):
        """Draw boss health bar at bottom center of screen"""
        if not boss:
            return
        
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        
        # Boss HP bar dimensions and position
        bar_width = 600
        bar_height = 40
        bar_x = (screen_width - bar_width) // 2
        bar_y = screen_height - 80
        
        # Calculate health ratio
        health_ratio = max(0, boss.health / boss.max_health)
        
        # Draw background
        bg_rect = pygame.Rect(bar_x - 10, bar_y - 10, bar_width + 20, bar_height + 40)
        pygame.draw.rect(self.display_surface, (20, 20, 30, 230), bg_rect)
        pygame.draw.rect(self.display_surface, (200, 0, 0), bg_rect, 3)
        
        # Draw health bar background
        pygame.draw.rect(self.display_surface, (60, 20, 20), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw health bar fill
        pygame.draw.rect(self.display_surface, (220, 20, 20), (bar_x, bar_y, bar_width * health_ratio, bar_height))
        
        # Draw border
        pygame.draw.rect(self.display_surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), 3)
        
        # Boss name text
        boss_name = self.font_large.render('BOSS', True, (255, 50, 50))
        boss_name_rect = boss_name.get_rect(center=(screen_width // 2, bar_y - 20))
        self.display_surface.blit(boss_name, boss_name_rect)
        
        # Health text
        health_text = self.font.render(f'{int(boss.health)}/{int(boss.max_health)}', True, (255, 255, 255))
        health_text_rect = health_text.get_rect(center=(screen_width // 2, bar_y + bar_height // 2))
        self.display_surface.blit(health_text, health_text_rect)

    def display(self):
        self.draw_health_bar()
        self.draw_stamina_bar()
        self.draw_level_and_exp()