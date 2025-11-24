import pygame 
from settings import *
import os

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
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
		self.image = self.idle_image.subsurface(pygame.Rect(
			(self.current_frame * self.frame_width)+self.frame_width//4,
			(self.current_row * self.frame_height)+self.frame_height//4,
			self.frame_width//2,
			self.frame_height//2
		))
		self.rect = self.image.get_rect(topleft = pos)
		self.anim_interval = 0

		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.orientation = 'right'

		self.attack_anim = False
		self.attack_frame = 0

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

			new_x = self.rect.x + self.direction.x * self.speed
			new_y = self.rect.y + self.direction.y * self.speed

			new_x = max(0, min(new_x, boundary_rect.width - self.rect.width))
			new_y = max(0, min(new_y, boundary_rect.height - self.rect.height))

			self.rect.x = new_x
			self.rect.y = new_y

	def attack(self):
		if self.attack_anim == False:
			self.speed -= 2
			self.attack_anim = True
			self.attack_frame = 4
			self.current_frame = 0

	def animate(self):
		if self.attack_anim:
			self.attack_frame -= 1
			if self.attack_frame <= 0:
				self.attack_anim = False
				self.speed += 2
			self.current_frame = (self.current_frame + 1) % 4
			self.update_sprite()
		else:
			self.current_frame = (self.current_frame + 1) % 8
			self.update_sprite()

	def update_sprite(self):
		if self.attack_anim:
			src_rect = pygame.Rect(
				(self.current_frame * self.frame_width)+self.frame_width//4,
				(self.current_row * self.frame_height)+self.frame_height//4,
				self.frame_width//2,
				self.frame_height//2
			)
			self.image = self.attack_image.subsurface(src_rect)
			if self.orientation == 'left':
				self.image = pygame.transform.flip(self.image, True, False)
			return
		else:
			src_rect = pygame.Rect(
            (self.current_frame * self.frame_width)+self.frame_width//4,
            (self.current_row * self.frame_height)+self.frame_height//4,
            self.frame_width//2,
            self.frame_height//2
        )
		self.image = self.idle_image.subsurface(src_rect)
		if self.orientation == 'left':
			self.image = pygame.transform.flip(self.image, True, False)

	def update(self, boundary_rect):
		self.input()
		self.move(boundary_rect)
		if self.anim_interval < 1:
			self.anim_interval += 0.1
		if self.anim_interval >= 1:
			self.anim_interval = 0
			self.animate()

	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)

	def debug_draw(self, surface):
		"""Draws a boundary around the player's rect for debugging."""
        # Draw the rectangle: (surface, color, rect, thickness)
        # 'yellow' or 'blue' are good choices, and 1 is the thickness in pixels.
		pygame.draw.rect(surface, 'yellow', self.rect, 1)
	
	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft)

class Hitbox(Player):
	def __init__(self, attack_image, pos, groups):
		super().__init__(pos, groups)
		