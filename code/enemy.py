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

        # Stats
        self.health = 200
        self.max_health = 200
        self.attack_power = 15
        self.defense = 2
        self.detection_radius = 300
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

        if distance < self.detection_radius and distance > 0:
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