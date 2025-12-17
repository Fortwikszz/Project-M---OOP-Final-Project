import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.invincible = False
        self.invincibility_duration = 10
		
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