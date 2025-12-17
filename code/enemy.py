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
        self.base_health = 500
        self.base_attack_power = 15
        self.base_defense = 2
        
        # Scale stats based on player level
        level_multiplier = 1 + (player.level - 1) * 0.15  # 15% increase per level
        self.health = int(self.base_health * level_multiplier)
        self.max_health = self.health
        self.attack_power = int(self.base_attack_power * level_multiplier)
        self.defense = int(self.base_defense * level_multiplier)
        
        self.detection_radius = 100
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
            if self.current_frame == 2:
                self.create_attack_hitbox(self)
            else:
                self.delete_attack_hitbox(self)
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

    def draw_health_bar(self, surface, camera_offset):
        """Draw health bar below the enemy"""
        if self.health <= 0:
            return
            
        # Health bar dimensions
        bar_width = 60
        bar_height = 6
        border_width = 1
        
        # Position below enemy's feet
        bar_x = self.rect.centerx - bar_width // 2 + camera_offset.x
        bar_y = self.rect.bottom - 20 + camera_offset.y
        
        # Calculate health percentage
        health_ratio = self.health / self.max_health
        
        # Draw background (dark red)
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 20, 20), background_rect)
        
        # Draw current health (green to red based on health)
        if health_ratio > 0.5:
            bar_color = (50, 200, 50)  # Green
        elif health_ratio > 0.25:
            bar_color = (255, 200, 0)  # Yellow
        else:
            bar_color = (220, 50, 50)  # Red
            
        health_rect = pygame.Rect(bar_x, bar_y, int(bar_width * health_ratio), bar_height)
        pygame.draw.rect(surface, bar_color, health_rect)
        
        # Draw border
        pygame.draw.rect(surface, (20, 20, 20), background_rect, border_width)

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


class Boss(Entity):
    """Boss enemy with high health and damage"""
    def __init__(self, pos, groups, obstacle_sprites, player, create_attack_hitbox, delete_attack_hitbox):
        super().__init__(groups)
        self.create_attack_hitbox = create_attack_hitbox
        self.delete_attack_hitbox = delete_attack_hitbox
        assets_path = os.path.join("assets", "Tiny Swords", "Tiny Swords (Update 010)", "Factions", "Knights", "Troops", "Warrior", "Red")
        self.full_image = pygame.image.load(os.path.join(assets_path, "Warrior_Red.png")).convert_alpha()
        self.idle_image = self.full_image.subsurface((0, 0, self.full_image.get_width(), self.full_image.get_height()//8))
        # Attack images - each should have 3 frames
        attack_width = self.full_image.get_width() // 2
        self.attack_image1 = self.full_image.subsurface((attack_width, self.full_image.get_height()//8*2, attack_width, self.full_image.get_height()//8))
        self.attack_image2 = self.full_image.subsurface((attack_width, self.full_image.get_height()//8*3, attack_width, self.full_image.get_height()//8))
        self.sheet_width, self.sheet_height = self.idle_image.get_size()
        self.frame_width = self.sheet_width // 6
        self.frame_height = self.sheet_height // 1
        
        # Attack frame width (3 frames per attack animation)
        self.attack_frame_width = attack_width // 3
        
        self.current_frame = 0
        temp_image = self.idle_image.subsurface(pygame.Rect(
            (self.current_frame * self.frame_width),
            (0),
            self.frame_width,
            self.frame_height
        ))
        self.image = pygame.transform.scale(temp_image, (256, 256))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, -60)
        self.anim_interval = 0

        self.direction = pygame.math.Vector2()
        self.speed = 1
        self.orientation = 'right'

        self.attack_anim = False
        self.attack_frame = 0
        self.attack_cooldown = 0

        self.obstacle_sprites = obstacle_sprites
        self.player = player

        # Boss stats
        self.health = 10000
        self.max_health = 10000
        self.attack_power = 50
        self.defense = 5
        self.detection_radius = 300
        self.attack_radius = 80
        
        # Invincibility frames
        self.invincibility_timer = 0
        self.invincibility_duration = 120
        
        # Attack animation phase tracking
        self.attack_phase = 0  # 0 = image1, 1 = image2, 2 = image1 again

    def ai_behavior(self):
        """AI logic to move towards player and attack when close - similar to Goblin"""
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
            self.speed -= 0.5
            self.attack_anim = True
            self.attack_frame = 9  # 9 frames total (3 frames x 3 phases)
            self.current_frame = 0
            self.attack_cooldown = 30
            self.attack_phase = 0  # Start with attack_image1
    
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
            
            # Transition between attack phases (3 frames each)
            # Phase 0: frames 9-7 (attack_image1)
            # Phase 1: frames 6-4 (attack_image2)
            # Phase 2: frames 3-1 (attack_image1 again)
            if self.attack_frame == 6:
                self.attack_phase = 1
                self.current_frame = 0
            elif self.attack_frame == 3:
                self.attack_phase = 2
                self.current_frame = 0
            
            if self.attack_frame <= 0:
                self.attack_anim = False
                self.speed += 0.5
                self.delete_attack_hitbox(self)
                self.attack_phase = 0
            
            self.current_frame = (self.current_frame + 1) % 3
            self.update_sprite()
        else:
            self.current_frame = (self.current_frame + 1) % 6
            self.update_sprite()

    def update_sprite(self):
        if self.attack_anim:
            # Choose the correct attack image based on phase
            if self.attack_phase == 0:
                current_attack_image = self.attack_image1
            elif self.attack_phase == 1:
                current_attack_image = self.attack_image2
            else:  # phase 2
                current_attack_image = self.attack_image1
            
            src_rect = pygame.Rect(
                self.current_frame * self.attack_frame_width,
                0,
                self.attack_frame_width,
                self.frame_height
            )
            temp_image = current_attack_image.subsurface(src_rect)
            temp_image = pygame.transform.scale(temp_image, (256, 256))
            if self.orientation == 'left':
                temp_image = pygame.transform.flip(temp_image, True, False)
            self.image = temp_image
            # Only create hitbox on second to last frame (frame 1 out of 0,1,2)
            if self.current_frame == 1:
                self.create_attack_hitbox(self)
            else:
                self.delete_attack_hitbox(self)
        else:
            self.delete_attack_hitbox(self)
            src_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            )
            temp_image = self.idle_image.subsurface(src_rect)
            temp_image = pygame.transform.scale(temp_image, (256, 256))
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