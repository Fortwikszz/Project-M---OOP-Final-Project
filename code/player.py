import pygame 
from code.settings import *
import os

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacle_sprites, create_attack_hitbox, delete_attack_hitbox):
		super().__init__(groups)
		# Use relative path from project root
		assets_path = os.path.join("assets", "Tiny Swords (Free Pack)", "Tiny Swords (Free Pack)", "Units", "Black Units", "Warrior")
		self.idle_image = pygame.image.load(os.path.join(assets_path, "Warrior_Idle.png")).convert_alpha()
		self.running_image = pygame.image.load(os.path.join(assets_path, "Warrior_Run.png")).convert_alpha()
		self.attack_image = pygame.image.load(os.path.join(assets_path, "Warrior_Attack1.png")).convert_alpha()
		self.sheet_width, self.sheet_height = self.idle_image.get_size()
		self.frame_width = self.sheet_width // 8
		self.frame_height = self.sheet_height // 1

		self.current_frame = 0
		self.current_row = 0
		self.is_moving = False
		temp_image = self.idle_image.subsurface(pygame.Rect(
			(self.current_frame * self.frame_width)+self.frame_width//8,
			(self.current_row * self.frame_height)+self.frame_height//8,
			self.frame_width*3//4,
			self.frame_height*3//4
		))
		self.image = pygame.transform.scale(temp_image, (96, 96))
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-20, -60)
		self.anim_interval = 0

		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.orientation = 'right'

		self.attack_anim = False
		self.attack_frame = 0
		self.create_attack_hitbox = create_attack_hitbox
		self.delete_attack_hitbox = delete_attack_hitbox

		self.obstacle_sprites = obstacle_sprites

		# stats
		self.health = 100
		self.max_health = 100
		self.stamina = 100
		self.max_stamina = 100
		self.attack_power = 10
		self.defense = 5
		
		# Invincibility frames
		self.invincibility_timer = 0
		self.invincibility_duration = 60  # 1 second at 60 FPS

	def input(self):
		keys = pygame.key.get_pressed()
		
		self.direction.x = 0
		self.direction.y = 0

		if (keys[pygame.K_UP] and not keys[pygame.K_DOWN]) or (keys[pygame.K_w] and not keys[pygame.K_s]):
			self.direction.y = -1
		elif (keys[pygame.K_DOWN] and not keys[pygame.K_UP]) or (keys[pygame.K_s] and not keys[pygame.K_w]):
			self.direction.y = 1
		if (keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]) or (keys[pygame.K_a] and not keys[pygame.K_d]):
			self.direction.x = -1
			if self.orientation != 'left':
				self.orientation = 'left'
		elif (keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]) or (keys[pygame.K_d] and not keys[pygame.K_a]):
			self.direction.x = 1
			if self.orientation != 'right':
				self.orientation = 'right'

	def move(self, boundary_rect):
		if self.direction.length_squared() > 0:
			if self.direction.length() != 0:
				self.direction = self.direction.normalize()

			new_x = self.hitbox.x + self.direction.x * self.speed
			new_y = self.hitbox.y + self.direction.y * self.speed

			# Keep player within map boundaries
			new_x = max(boundary_rect.left, min(new_x, boundary_rect.right - self.hitbox.width))
			new_y = max(boundary_rect.top, min(new_y, boundary_rect.bottom - self.hitbox.height))

			self.hitbox.x = new_x
			self.collide('horizontal')
			self.hitbox.y = new_y
			self.collide('vertical')
			self.rect.center = self.hitbox.center

	def attack(self):
		if self.attack_anim == False and self.stamina >= 10:
			self.speed -= 2
			self.attack_anim = True
			self.attack_frame = 4
			self.current_frame = 0
			self.stamina -= 10

	def collide(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.rect.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.rect.right
		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.rect.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.rect.bottom

	def animate(self):
		if self.attack_anim:
			self.attack_frame -= 1
			if self.attack_frame <= 0:
				self.attack_anim = False
				self.speed += 2
				self.delete_attack_hitbox()  # Remove attack hitbox when attack ends
			self.current_frame = (self.current_frame + 1) % 4
			self.update_sprite()
		else:
			self.current_frame = (self.current_frame + 1) % 8
			self.update_sprite()

		self.stamina = min(self.stamina + 0.5, self.max_stamina)

	def update_sprite(self):
		if self.attack_anim:
			src_rect = pygame.Rect(
				(self.current_frame * self.frame_width)+self.frame_width//8,
				(self.current_row * self.frame_height)+self.frame_height//8,
				self.frame_width*3//4,
				self.frame_height*3//4
			)
			temp_image = self.attack_image.subsurface(src_rect)
			temp_image = pygame.transform.scale(temp_image, (96, 96))
			if self.orientation == 'left':
				temp_image = pygame.transform.flip(temp_image, True, False)
			self.image = temp_image
			self.create_attack_hitbox()
			return
		else:
			src_rect = pygame.Rect(
				(self.current_frame * self.frame_width)+self.frame_width//8,
				(self.current_row * self.frame_height)+self.frame_height//8,
				self.frame_width*3//4,
				self.frame_height*3//4
			)
			temp_image = self.idle_image.subsurface(src_rect)
			temp_image = pygame.transform.scale(temp_image, (96, 96))
			if self.orientation == 'left':
				temp_image = pygame.transform.flip(temp_image, True, False)
			self.image = temp_image
			self.delete_attack_hitbox()

	def update(self, boundary_rect):
		self.input()
		self.move(boundary_rect)
		if self.anim_interval < 1:
			self.anim_interval += 0.1
		if self.anim_interval >= 1:
			self.anim_interval = 0
			self.animate()
		
		# Update invincibility timer
		if self.invincibility_timer > 0:
			self.invincibility_timer -= 1
	
	def take_damage(self, damage):
		if self.invincibility_timer <= 0:
			actual_damage = max(1, damage - self.defense)
			self.health -= actual_damage
			if self.health < 0:
				self.health = 0
			self.invincibility_timer = self.invincibility_duration

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)

	def debug_draw(self, surface):
		"""Draws a boundary around the player's hitbox for debugging."""
        # Draw the rectangle: (surface, color, rect, thickness)
        # 'yellow' or 'blue' are good choices, and 1 is the thickness in pixels.
		pygame.draw.rect(surface, 'yellow', self.hitbox, 1)
		pygame.draw.rect(surface, 'blue', self.rect, 1)
	
	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)

class AttackHitbox(pygame.sprite.Sprite):
	def __init__(self, player, groups):
		super().__init__(groups)
		orientation = player.orientation
		self.image = pygame.Surface((96, 96), pygame.SRCALPHA)
		if orientation == 'right':
			self.image.fill((255, 0, 0, 100))  # Semi-transparent red
			self.rect = self.image.get_rect(center = (player.rect.right, player.rect.centery - 10))
		else:
			self.image.fill((255, 0, 0, 100))  # Semi-transparent red
			self.rect = self.image.get_rect(center = (player.rect.left, player.rect.centery - 10))