import pygame
from code.settings import *
from code.tiled import Tile
from code.player import Player, AttackHitbox
from code.enemy import Goblin
from code.ui import UI
import pytmx
import os
import random

class Level:
    def __init__(self):
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.visible_sprites = YsortCameraGroup()
        self.ground_sprites = pygame.sprite.Group()  # Ground tiles (no Y-sort)
        self.decoration_sprites = pygame.sprite.Group()  # Decoration tiles (Y-sort)
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()  # Enemy group
        
        # sprite setup
        self.create_map()

        # attack hitbox
        self.current_attack_hitbox = None
        self.goblin_attack_hitboxes = {}  # Track goblin attack hitboxes
        
        # Goblin spawning
        self.spawn_timer = 0
        self.spawn_interval = 300  # 5 seconds at 60 FPS
        self.max_goblins = 3
        
    def create_map(self):
        # Load TMX map file
        tmx_path = os.path.join('assets', 'maps', 'Inimapbang1.tmx')
        tmx_data = pytmx.load_pygame(tmx_path)
        
        # Store map dimensions for boundary
        self.map_width = tmx_data.width * TILESIZE
        self.map_height = tmx_data.height * TILESIZE
        self.map_rect = pygame.Rect(0, 0, self.map_width, self.map_height)
        
        # Track current attack hitbox
        self.current_attack_hitbox = None
        
        # Create player at a starting position
        self.player = Player((128, 128), [self.visible_sprites, self.decoration_sprites], self.obstacle_sprites, self.create_attack_hitbox, self.delete_attack_hitbox)

        self.ui = UI(self.player)
        
        # Render all layers
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Check if layer is Decoration layer for Y-sorting
                        if layer.name == 'Decoration':
                            Tile((x * TILESIZE, y * TILESIZE), [self.visible_sprites, self.decoration_sprites], tile)
                        else:
                            Tile((x * TILESIZE, y * TILESIZE), [self.visible_sprites, self.ground_sprites], tile)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.image:
                        scaled_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))
                        Tile((obj.x, obj.y), [self.visible_sprites, self.decoration_sprites, self.obstacle_sprites], scaled_image)
        
    def run(self):
        self.visible_sprites.update(self.map_rect) 
        self.visible_sprites.custom_draw(self.player, self.ground_sprites, self.decoration_sprites)
        self.ui.display()
        
        # Spawn goblins
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            if len(self.enemy_sprites) < self.max_goblins:
                self.spawn_goblin()
            self.spawn_timer = 0
        
        # Check player attack hitting goblins
        if self.current_attack_hitbox:
            for goblin in self.enemy_sprites:
                if self.current_attack_hitbox.rect.colliderect(goblin.hitbox):
                    goblin.take_damage(self.player.attack_power)
        
        # Check goblin attacks hitting player
        for goblin, hitbox in list(self.goblin_attack_hitboxes.items()):
            if hitbox and hitbox.rect.colliderect(self.player.hitbox):
                self.player.take_damage(goblin.attack_power)
        
        # Remove dead goblins
        for goblin in self.enemy_sprites.copy():
            if goblin.health <= 0:
                goblin.kill()
                if goblin in self.goblin_attack_hitboxes:
                    if self.goblin_attack_hitboxes[goblin]:
                        self.goblin_attack_hitboxes[goblin].kill()
                    del self.goblin_attack_hitboxes[goblin]

    def create_attack_hitbox(self):
        # Delete previous hitbox if it exists
        if self.current_attack_hitbox:
            self.current_attack_hitbox.kill()
        self.current_attack_hitbox = AttackHitbox(self.player, [self.visible_sprites, self.decoration_sprites])
    
    def delete_attack_hitbox(self):
        if self.current_attack_hitbox:
            self.current_attack_hitbox.kill()
            self.current_attack_hitbox = None

    def delete_attack_hitbox(self):
        if self.current_attack_hitbox:
            self.current_attack_hitbox.kill()
        self.current_attack_hitbox = None
    
    def spawn_goblin(self):
        # Random spawn position away from player
        margin = 200
        while True:
            x = random.randint(margin, self.map_width - margin)
            y = random.randint(margin, self.map_height - margin)
            if abs(x - self.player.rect.centerx) > 300 or abs(y - self.player.rect.centery) > 300:
                break
        
        goblin = Goblin((x, y), [self.visible_sprites, self.decoration_sprites, self.enemy_sprites], 
                       self.obstacle_sprites, self.player, self.create_goblin_attack_hitbox, self.delete_goblin_attack_hitbox)
        self.goblin_attack_hitboxes[goblin] = None
    
    def create_goblin_attack_hitbox(self, goblin):
        # Delete previous hitbox if it exists
        if goblin in self.goblin_attack_hitboxes and self.goblin_attack_hitboxes[goblin]:
            self.goblin_attack_hitboxes[goblin].kill()
        self.goblin_attack_hitboxes[goblin] = GoblinAttackHitbox(goblin, [self.visible_sprites, self.decoration_sprites])
    
    def delete_goblin_attack_hitbox(self, goblin):
        if goblin in self.goblin_attack_hitboxes and self.goblin_attack_hitboxes[goblin]:
            self.goblin_attack_hitboxes[goblin].kill()
            self.goblin_attack_hitboxes[goblin] = None

class GoblinAttackHitbox(pygame.sprite.Sprite):
    def __init__(self, goblin, groups):
        super().__init__(groups)
        orientation = goblin.orientation
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        if orientation == 'right':
            self.image.fill((255, 165, 0, 100))  # Semi-transparent orange
            self.rect = self.image.get_rect(center=(goblin.rect.right, goblin.rect.centery))
        else:
            self.image.fill((255, 165, 0, 100))  # Semi-transparent orange
            self.rect = self.image.get_rect(center=(goblin.rect.left, goblin.rect.centery))

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, ground_sprites, decoration_sprites):
        # Calculate offset based on player position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw ground sprites first (no Y-sort needed)
        for sprite in ground_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        # Draw decoration sprites with Y-sort (includes player)
        for sprite in sorted(decoration_sprites, key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)