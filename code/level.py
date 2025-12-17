import pygame
from code.settings import *
from code.tiled import Tile
from code.player import Player, AttackHitbox
from code.enemy import Goblin, Boss
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
        self.interactable_sprites = pygame.sprite.Group()  # Interactable objects
        
        # sprite setup
        self.create_map()

        # attack hitbox
        self.current_attack_hitbox = None
        self.goblin_attack_hitboxes = {}  # Track goblin attack hitboxes
        
        # Goblin spawning
        self.spawn_timer = 0
        self.spawn_interval = 150  # 2.5 seconds at 60 FPS
        self.base_max_enemies = 5
        self.max_goblins = self.base_max_enemies
        
        # Interaction tracking
        self.near_interactable = None

        # Arena and Boss tracking
        self.arena = "Mob"
        self.boss = None
        self.boss_spawned = False
        
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
        
        # Default player spawn position
        player_pos = (1024, 1700)
        
        # Create player at spawn position
        self.player = Player(player_pos, [self.visible_sprites, self.decoration_sprites], self.obstacle_sprites, self.create_attack_hitbox, self.delete_attack_hitbox)

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
                        # Check if object is interactable via custom properties
                        is_interactable = obj.properties.get('interactable', False)
                        if is_interactable:
                            # Create interactable object
                            InteractableObject(
                                (obj.x, obj.y), 
                                [self.visible_sprites, self.decoration_sprites, self.interactable_sprites, self.obstacle_sprites],
                                scaled_image,
                                obj.properties.get('name', 'Object'),
                                obj.properties.get('message', 'An interactable object.')
                            )
                        else:
                            # Regular obstacle
                            Tile((obj.x, obj.y), [self.visible_sprites, self.decoration_sprites, self.obstacle_sprites], scaled_image)

    def change_map(self, new_map_path, player_spawn_pos):
        # Clear existing sprites
        self.visible_sprites.empty()
        self.ground_sprites.empty()
        self.decoration_sprites.empty()
        self.obstacle_sprites.empty()
        self.enemy_sprites.empty()
        self.interactable_sprites.empty()
        self.goblin_attack_hitboxes.clear()
        self.current_attack_hitbox = None
        self.near_interactable = None
        
        # Change music based on map
        if 'Boss_field' in new_map_path or 'boss_field' in new_map_path:
            # Play boss fight music
            try:
                boss_music_path = os.path.join("audio", "boss_fight.mp3")
                if os.path.exists(boss_music_path):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(boss_music_path)
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    print(f"Playing boss fight music from {boss_music_path}")
                else:
                    print(f"Boss fight music not found: {boss_music_path}")
            except Exception as e:
                print(f"Warning: Could not load boss fight music: {e}")
        else:
            # Play normal background music for regular maps
            try:
                bg_music_path = os.path.join("audio", "background.mp3")
                if os.path.exists(bg_music_path):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(bg_music_path)
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    print(f"Playing background music from {bg_music_path}")
                else:
                    print(f"Background music not found: {bg_music_path}")
            except Exception as e:
                print(f"Warning: Could not load background music: {e}")
        
        # Load new TMX map file
        new_map_path = os.path.join('assets', 'maps', new_map_path)
        tmx_data = pytmx.load_pygame(new_map_path)
        
        # Store map dimensions for boundary
        self.map_width = tmx_data.width * TILESIZE
        self.map_height = tmx_data.height * TILESIZE
        self.map_rect = pygame.Rect(0, 0, self.map_width, self.map_height)
        
        # Create player at new spawn position
        self.player.rect.topleft = player_spawn_pos
        self.player.hitbox.topleft = player_spawn_pos
        self.visible_sprites.add(self.player)
        self.decoration_sprites.add(self.player)
        
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
                        # Check if object is interactable via custom properties
                        is_interactable = obj.properties.get('interactable', False)
                        if is_interactable:
                            # Create interactable object
                            InteractableObject(
                                (obj.x, obj.y), 
                                [self.visible_sprites, self.decoration_sprites, self.interactable_sprites, self.obstacle_sprites],
                                scaled_image,
                                obj.properties.get('name', 'Object'),
                                obj.properties.get('message', 'An interactable object.')
                            )
                        else:
                            Tile((obj.x, obj.y), [self.visible_sprites, self.decoration_sprites, self.obstacle_sprites], scaled_image)
        
    def run(self):
        if self.arena == "Mob":
            self.visible_sprites.update(self.map_rect) 
            self.visible_sprites.custom_draw(self.player, self.ground_sprites, self.decoration_sprites, self.map_rect)
            self.ui.display()
            
            # Check collision with interactable objects
            self.near_interactable = None
            for interactable in self.interactable_sprites:
                if self.player.rect.colliderect(interactable.rect):
                    self.near_interactable = interactable
                    break
            
            # Display interaction prompt if near an object
            if self.near_interactable:
                self.ui.display_interaction_prompt()
            
            # Handle interaction (E key)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] and self.near_interactable:
                self.near_interactable.interact(self, self.change_map)
            
            # Check if player is dead
            if self.player.health <= 0:
                return {'game_over': True}
            
            # Update difficulty based on player level
            self.update_difficulty()
            
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
                        if goblin.invincibility_timer <= 0:
                            goblin.take_damage(self.player.attack_power)
            
            # Check goblin attacks hitting player
            for goblin, hitbox in list(self.goblin_attack_hitboxes.items()):
                if hitbox and hitbox.rect.colliderect(self.player.hitbox):
                    if self.player.invincibility_timer <= 0:
                        self.player.take_damage(goblin.attack_power)
            
            # Remove dead goblins and give exp
            for goblin in self.enemy_sprites.copy():
                if goblin.health <= 0:
                    self.player.gain_exp(20)  # 20 exp per kill
                    goblin.kill()
                    if goblin in self.goblin_attack_hitboxes:
                        if self.goblin_attack_hitboxes[goblin]:
                            self.goblin_attack_hitboxes[goblin].kill()
                        del self.goblin_attack_hitboxes[goblin]

        if self.arena == "Boss":
            self.visible_sprites.update(self.map_rect) 
            self.visible_sprites.custom_draw(self.player, self.ground_sprites, self.decoration_sprites, self.map_rect)
            self.ui.display()
            
            # Display boss HP bar
            if self.boss:
                self.ui.draw_boss_health_bar(self.boss)

            if self.player.health <= 0:
                return {'game_over': True}
            
            # Check player attack hitting boss
            if self.current_attack_hitbox and self.boss:
                if self.current_attack_hitbox.rect.colliderect(self.boss.hitbox):
                    if self.boss.invincibility_timer <= 0:
                        self.boss.take_damage(self.player.attack_power)
            
            # Check boss attack hitting player
            if self.boss and self.boss in self.goblin_attack_hitboxes:
                hitbox = self.goblin_attack_hitboxes[self.boss]
                if hitbox and hitbox.rect.colliderect(self.player.hitbox):
                    if self.player.invincibility_timer <= 0:
                        self.player.take_damage(self.boss.attack_power)
            
            # Check if boss is dead
            if self.boss and self.boss.health <= 0:
                self.player.gain_exp(200)  # Big exp reward for boss kill
                self.boss.kill()
                if self.boss in self.goblin_attack_hitboxes:
                    if self.goblin_attack_hitboxes[self.boss]:
                        self.goblin_attack_hitboxes[self.boss].kill()
                    del self.goblin_attack_hitboxes[self.boss]
                self.boss = None
                self.boss_spawned = False
                self.arena = "Mob"  # Return to mob arena
                # Change map back to original map
                self.change_map('Inimapbang1.tmx', (1024, 1700))
    
    def update_difficulty(self):
        """Update difficulty based on player level"""
        # Every level, increase max enemies
        level_tier = (self.player.level - 1)
        self.max_goblins = self.base_max_enemies + level_tier
    
    def spawn_goblin(self):
        """Spawn goblin enemy"""
        # Random spawn position away from player
        margin = 200
        attempts = 0
        while attempts < 10:
            x = random.randint(margin, self.map_width - margin)
            y = random.randint(margin, self.map_height - margin)
            if abs(x - self.player.rect.centerx) > 300 or abs(y - self.player.rect.centery) > 300:
                break
            attempts += 1
        
        goblin = Goblin((x, y), [self.visible_sprites, self.decoration_sprites, self.enemy_sprites], 
                       self.obstacle_sprites, self.player, self.create_goblin_attack_hitbox, self.delete_goblin_attack_hitbox)
        self.goblin_attack_hitboxes[goblin] = None

    def spawn_boss(self):
        """Spawn boss enemy in center of map"""
        boss_x = self.map_width // 2
        boss_y = self.map_height // 2
        self.boss = Boss((boss_x, boss_y), [self.visible_sprites, self.decoration_sprites, self.enemy_sprites], 
                    self.obstacle_sprites, self.player, self.create_goblin_attack_hitbox, self.delete_goblin_attack_hitbox)
        self.goblin_attack_hitboxes[self.boss] = None
    
    def create_attack_hitbox(self):
        # Delete previous hitbox if it exists
        if self.current_attack_hitbox:
            self.current_attack_hitbox.kill()
        self.current_attack_hitbox = AttackHitbox(self.player, [self.visible_sprites, self.decoration_sprites])

    def delete_attack_hitbox(self):
        if self.current_attack_hitbox:
            self.current_attack_hitbox.kill()
            self.current_attack_hitbox = None
    
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
        # Completely transparent - no visible color
        self.image.fill((0, 0, 0, 0))
        if orientation == 'right':
            self.rect = self.image.get_rect(center=(goblin.rect.right, goblin.rect.centery))
        else:
            self.rect = self.image.get_rect(center=(goblin.rect.left, goblin.rect.centery))

class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image, name, message):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-100, -100)  # Slightly smaller hitbox for better collision
        self.name = name
        self.message = message
    
    def interact(self, level, change_map):
        level.arena = "Boss"
        change_map('Boss_field.tmx', (500, 500))
        level.spawn_boss()

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, ground_sprites, decoration_sprites, map_rect):
        # Calculate offset based on player position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # Clamp camera to map boundaries
        # Don't let camera show area outside the map
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        
        # If map is smaller than screen, center it
        if map_rect.width < screen_width:
            self.offset.x = (map_rect.width - screen_width) // 2
        else:
            # Clamp camera so it doesn't go beyond map edges
            self.offset.x = max(0, min(self.offset.x, map_rect.width - screen_width))
        
        if map_rect.height < screen_height:
            self.offset.y = (map_rect.height - screen_height) // 2
        else:
            self.offset.y = max(0, min(self.offset.y, map_rect.height - screen_height))

        # Draw ground sprites first (no Y-sort needed)
        for sprite in ground_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        # Draw all visible sprites with Y-sort (includes player, enemies, portals, decorations)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            if sprite not in ground_sprites:  # Don't draw ground sprites twice
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
        
        # Draw health bars for enemies (Goblin only, not Boss)
        from code.enemy import Goblin
        for sprite in self.sprites():
            if isinstance(sprite, Goblin):
                sprite.draw_health_bar(self.display_surface, -self.offset)