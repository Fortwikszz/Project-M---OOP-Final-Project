import pygame
from code.settings import *
from code.tiled import Tile
from code.player import Player, AttackHitbox
import pytmx
import os

class Level:
    def __init__(self):
        
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.visible_sprites = YsortCameraGroup()
        self.ground_sprites = pygame.sprite.Group()  # Ground tiles (no Y-sort)
        self.decoration_sprites = pygame.sprite.Group()  # Decoration tiles (Y-sort)
        self.obstacle_sprites = pygame.sprite.Group()
        
        # sprite setup
        self.create_map()

        # attack hitbox
        self.current_attack_hitbox = None
        
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