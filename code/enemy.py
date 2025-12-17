import pygame
from code.entity import Entity
import os

class Goblin(Entity):
    def __init__(self, pos, groups, obstacle_sprites, player, create_attack_hitbox, delete_attack_hitbox):
        super().__init__(groups)
        self.create_attack_hitbox = create_attack_hitbox
        self.delete_attack_hitbox = delete_attack_hitbox
        assets_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "Factions", "Goblins", "Troops", "Torch", "Purple")
        self.full_image = pygame.image.load(os.path.join(assets_path, "Torch_Purple.png")).convert_alpha()
        self.idle_image = self.full_image.subsurface((0, 0, self.full_image.get_width(), self.full_image.get_height()//5))
        self.attack_image = self.full_image.subsurface((0, self.full_image.get_height()//5*2, self.full_image.get_width(), self.full_image.get_height()//5))
        self.sheet_width, self.sheet_height = self.idle_image.get_size()
        self.frame_width = self.sheet_width // 7
        self.frame_height = self.sheet_height // 1
        
        # Load sound effects
        self.attack_sound = None
        try:
            audio_path = os.path.join("audio", "torch_slash.mp3")
            if os.path.exists(audio_path):
                self.attack_sound = pygame.mixer.Sound(audio_path)
                self.attack_sound.set_volume(0.4)
                print(f"Loaded torch_slash sound from {audio_path}")
            else:
                print(f"Sound file not found: {audio_path}")
        except Exception as e:
            print(f"Warning: Could not load torch_slash sound: {e}")

        self.current_frame = 0
        self.current_row = 0
        temp_image = self.idle_image.subsurface(pygame.Rect(
            (self.current_frame * self.frame_width),
            (self.current_row * self.frame_height),
            self.frame_width,
            self.frame_height
        ))
        self.image = pygame.transform.scale(temp_image, (128, 128))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -30)
        self.anim_interval = 0

        self.direction = pygame.math.Vector2()
        self.speed = 2
        self.orientation = 'right'

        self.attack_anim = False
        self.attack_frame = 0
        self.attack_cooldown = 0

        self.obstacle_sprites = obstacle_sprites
        self.player = player

        # Stats - will be scaled based on player level
        self.base_health = 200
        self.base_attack_power = 15
        self.base_defense = 2
        
        # Scale stats based on player level
        level_multiplier = 1 + (player.level - 1) * 0.15  # 15% increase per level
        self.health = int(self.base_health * level_multiplier)
        self.max_health = self.health
        self.attack_power = int(self.base_attack_power * level_multiplier)
        self.defense = int(self.base_defense * level_multiplier)
        
        self.detection_radius = 10000  # Always detect player
        self.attack_radius = 60
        
        # Invincibility frames
        self.invincibility_timer = 0
        self.invincibility_duration = 90

    def ai_behavior(self):
        """AI logic to move towards player and attack when close"""
        # Calculate distance to player
        player_vector = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        distance = player_vector.length()

        # Reset direction
        self.direction.x = 0
        self.direction.y = 0

        # Always chase player (no detection radius limit)
        if distance > 0:
            if distance > self.attack_radius:
                # Move towards player
                self.direction = player_vector.normalize()
                
                # Update orientation based on movement
                if self.direction.x > 0:
                    self.orientation = 'right'
                elif self.direction.x < 0:
                    self.orientation = 'left'
            else:
                # Close enough to attack
                if self.attack_cooldown <= 0 and not self.attack_anim:
                    self.attack()

    def attack(self):
        if not self.attack_anim:
            self.speed -= 1
            self.attack_anim = True
            self.attack_frame = 4
            self.current_frame = 0
            self.attack_cooldown = 15
            # Play attack sound
            if self.attack_sound:
                self.attack_sound.play()
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0

    def animate(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_anim:
            self.attack_frame -= 1
            if self.attack_frame <= 0:
                self.attack_anim = False
                self.speed += 1
                self.delete_attack_hitbox(self)
            self.current_frame = (self.current_frame + 1) % 6
            self.update_sprite()
        else:
            self.current_frame = (self.current_frame + 1) % 7
            self.update_sprite()

    def update_sprite(self):
        if self.attack_anim:
            src_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            temp_image = self.attack_image.subsurface(src_rect)
            temp_image = pygame.transform.scale(temp_image, (128, 128))
            if self.orientation == 'left':
                temp_image = pygame.transform.flip(temp_image, True, False)
            self.image = temp_image
            self.create_attack_hitbox(self)
        else:
            self.delete_attack_hitbox(self)
            src_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            temp_image = self.idle_image.subsurface(src_rect)
            temp_image = pygame.transform.scale(temp_image, (128, 128))
            if self.orientation == 'left':
                temp_image = pygame.transform.flip(temp_image, True, False)
            self.image = temp_image

    def update(self, boundary_rect):
        self.ai_behavior()
        self.move(boundary_rect)
        if self.anim_interval < 1:
            self.anim_interval += 0.1
        if self.anim_interval >= 1:
            self.anim_interval = 0
            self.animate()
        
        # Update invincibility timer
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1


class Dynamite(pygame.sprite.Sprite):
    """Projectile thrown by TNT Goblin"""
    def __init__(self, pos, target_pos, groups, damage):
        super().__init__(groups)
        
        # Try to load dynamite sprite, fallback to simple sprite if not found
        try:
            assets_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "Factions", "Goblins", "Troops", "TNT", "Dynamite")
            dynamite_image = pygame.image.load(os.path.join(assets_path, "Dynamite.png")).convert_alpha()
            
            # Dynamite.png has 8 frames horizontally
            self.frame_width = dynamite_image.get_width() // 8
            self.frame_height = dynamite_image.get_height()
            self.dynamite_sheet = dynamite_image
            self.has_sprite = True
        except:
            # Fallback: create a simple red circle
            self.has_sprite = False
            self.dynamite_sheet = None
        
        self.current_frame = 0
        self.anim_interval = 0
        
        # Initial image
        if self.has_sprite:
            temp_image = self.dynamite_sheet.subsurface(pygame.Rect(0, 0, self.frame_width, self.frame_height))
            self.image = pygame.transform.scale(temp_image, (32, 32))
        else:
            # Simple red circle as fallback
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 50, 50), (16, 16), 12)
        
        self.rect = self.image.get_rect(center=pos)
        
        # Movement
        self.pos = pygame.math.Vector2(pos)
        direction = pygame.math.Vector2(target_pos) - self.pos
        if direction.length() > 0:
            self.velocity = direction.normalize() * 5
        else:
            self.velocity = pygame.math.Vector2(0, 0)
        
        self.damage = damage
        self.lifetime = 120  # 2 seconds at 60 FPS
        
    def animate(self):
        if self.has_sprite:
            self.current_frame = (self.current_frame + 1) % 8
            src_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            temp_image = self.dynamite_sheet.subsurface(src_rect)
            self.image = pygame.transform.scale(temp_image, (32, 32))
    
    def update(self, boundary_rect=None):
        # Move
        self.pos += self.velocity
        self.rect.center = self.pos
        
        # Animate
        if self.anim_interval < 1:
            self.anim_interval += 0.2
        if self.anim_interval >= 1:
            self.anim_interval = 0
            self.animate()
        
        # Decrease lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class TNTGoblin(Entity):
    """Ranged goblin that throws dynamite"""
    def __init__(self, pos, groups, obstacle_sprites, player, spawn_projectile):
        super().__init__(groups)
        self.spawn_projectile = spawn_projectile
        
        assets_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "Factions", "Goblins", "Troops", "Torch", "Purple")
        self.full_image = pygame.image.load(os.path.join(assets_path, "Torch_Purple.png")).convert_alpha()
        
        # Use Torch_Purple.png structure (same as regular Goblin)
        self.idle_image = self.full_image.subsurface((0, 0, self.full_image.get_width(), self.full_image.get_height()//5))
        self.attack_image = self.full_image.subsurface((0, self.full_image.get_height()//5*2, self.full_image.get_width(), self.full_image.get_height()//5))
        
        self.sheet_width, self.sheet_height = self.idle_image.get_size()
        self.frame_width = self.sheet_width // 7
        self.frame_height = self.sheet_height // 1

        self.current_frame = 0
        temp_image = self.idle_image.subsurface(pygame.Rect(0, 0, self.frame_width, self.frame_height))
        self.image = pygame.transform.scale(temp_image, (128, 128))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -30)
        self.anim_interval = 0

        self.direction = pygame.math.Vector2()
        self.speed = 1.5  # Slower than regular goblin
        self.orientation = 'right'

        self.attack_anim = False
        self.attack_frame = 0
        self.attack_cooldown = 0

        self.obstacle_sprites = obstacle_sprites
        self.player = player

        # Stats - stronger but slower
        self.health = 150
        self.max_health = 150
        self.attack_power = 25
        self.defense = 1
        self.detection_radius = 400  # Longer detection range
        self.attack_radius = 250  # Can attack from distance
        self.min_distance = 150  # Keeps distance from player
        
        # Invincibility frames
        self.invincibility_timer = 0
        self.invincibility_duration = 60

    def ai_behavior(self):
        """AI logic - keep distance and throw TNT"""
        player_vector = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        distance = player_vector.length()

        self.direction.x = 0
        self.direction.y = 0

        if distance < self.detection_radius and distance > 0:
            if distance < self.min_distance:
                # Too close - back away
                self.direction = -player_vector.normalize()
                
                # Update orientation
                if self.direction.x > 0:
                    self.orientation = 'right'
                elif self.direction.x < 0:
                    self.orientation = 'left'
            elif distance > self.attack_radius:
                # Too far - move closer
                self.direction = player_vector.normalize()
                
                # Update orientation
                if self.direction.x > 0:
                    self.orientation = 'right'
                elif self.direction.x < 0:
                    self.orientation = 'left'
            else:
                # In range - attack
                if self.attack_cooldown <= 0 and not self.attack_anim:
                    self.attack()

    def attack(self):
        """Throw dynamite"""
        if not self.attack_anim:
            self.speed -= 0.5
            self.attack_anim = True
            self.attack_frame = 4
            self.current_frame = 0
            self.attack_cooldown = 120  # Longer cooldown than melee
            
            # Spawn dynamite projectile
            try:
                self.spawn_projectile(self.rect.center, self.player.rect.center, self.attack_power)
            except Exception as e:
                print(f"Error spawning projectile: {e}")
                pass
    
    def take_damage(self, damage):
        if self.invincibility_timer <= 0:
            actual_damage = max(1, damage - self.defense)
            self.health -= actual_damage
            if self.health < 0:
                self.health = 0
            self.invincibility_timer = self.invincibility_duration

    def animate(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_anim:
            self.attack_frame -= 1
            if self.attack_frame <= 0:
                self.attack_anim = False
                self.speed += 0.5
            self.current_frame = (self.current_frame + 1) % 6
            self.update_sprite()
        else:
            self.current_frame = (self.current_frame + 1) % 7
            self.update_sprite()

    def update_sprite(self):
        if self.attack_anim:
            src_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            temp_image = self.attack_image.subsurface(src_rect)
            temp_image = pygame.transform.scale(temp_image, (128, 128))
            if self.orientation == 'left':
                temp_image = pygame.transform.flip(temp_image, True, False)
            self.image = temp_image
        else:
            src_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            temp_image = self.idle_image.subsurface(src_rect)
            temp_image = pygame.transform.scale(temp_image, (128, 128))
            if self.orientation == 'left':
                temp_image = pygame.transform.flip(temp_image, True, False)
            self.image = temp_image

    def update(self, boundary_rect):
        self.ai_behavior()
        self.move(boundary_rect)
        if self.anim_interval < 1:
            self.anim_interval += 0.1
        if self.anim_interval >= 1:
            self.anim_interval = 0
            self.animate()
        
        # Update invincibility timer
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1