import pygame, sys
import os
from code.settings import *
from code.level import *
from code.ui import Menu, PauseMenu, GameOverMenu

# Initialize pygame and mixer properly
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

# Test mixer
print(f"Pygame mixer initialized: {pygame.mixer.get_init()}")
print(f"Mixer channels: {pygame.mixer.get_num_channels()}")


class Game:
	def __init__(self):
     
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Projeect M')
		self.clock = pygame.time.Clock()

		# game states
		self.state = 'menu'  # 'menu', 'playing', or 'paused'
		self.menu = Menu()
		self.pause_menu = PauseMenu()
		self.game_over_menu = GameOverMenu()
		self.level = None
	
	def show_menu(self):
		# Play background music from the start
		print("show_menu() called - attempting to play background music...")
		try:
			music_path = os.path.join("audio", "background.mp3")
			print(f"Looking for background music at: {music_path}")
			print(f"File exists: {os.path.exists(music_path)}")
			
			if os.path.exists(music_path):
				pygame.mixer.music.stop()
				pygame.mixer.music.load(music_path)
				pygame.mixer.music.set_volume(0.2)
				pygame.mixer.music.play(-1)
				print(f"Successfully loaded and playing background music")
			else:
				print(f"Background music not found: {music_path}")
		except Exception as e:
			print(f"Error loading background music: {e}")
			import traceback
			traceback.print_exc()
		
		while self.state == 'menu':
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			
			# Handle menu input
			choice = self.menu.handle_input()
			
			if choice == 0:  # Start Game
				self.state = 'playing'
				# Music sudah playing background dari menu, jadi tidak perlu stop/restart
				self.level = Level()  # Initialize level when starting game
			elif choice == 1:  # Quit
				pygame.quit()
				sys.exit()
			
			# Draw menu
			self.menu.display()
			pygame.display.flip()
			self.clock.tick(FPS)
	
	def show_pause_menu(self):
		esc_pressed = False
		while self.state == 'paused':
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if not esc_pressed:
							esc_pressed = True
							self.state = 'playing'
							pygame.time.wait(200)
							return
			
			# Handle pause menu input
			choice = self.pause_menu.handle_input()
			
			if choice == 0:  # Continue
				self.state = 'playing'
				pygame.time.wait(200)
				return
			elif choice == 1:  # Main Menu
				self.state = 'menu'
				self.show_menu()
				return
			elif choice == 2:  # Quit
				pygame.quit()
				sys.exit()
			
			# Draw game in background
			self.screen.fill('black')
			self.level.visible_sprites.custom_draw(self.level.player, self.level.ground_sprites, self.level.decoration_sprites, self.level.map_rect)
			self.level.ui.display()
			
			# Draw pause menu on top
			self.pause_menu.display()
			pygame.display.flip()
			self.clock.tick(FPS)
	
	def show_game_over(self):
		while self.state == 'game_over':
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			
			# Handle game over menu input
			choice = self.game_over_menu.handle_input()
			
			if choice == 0:  # Restart
				self.state = 'playing'
				self.level = Level()  # Create new level
				pygame.time.wait(200)
				return
			elif choice == 1:  # Main Menu
				self.state = 'menu'
				self.show_menu()
				return
			elif choice == 2:  # Quit
				pygame.quit()
				sys.exit()
			
			# Draw game over screen
			self.screen.fill('black')
			self.game_over_menu.display()
			pygame.display.flip()
			self.clock.tick(FPS)
	
	def run(self):
		# Show menu first
		self.show_menu()
		
		# Game loop
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						self.level.player.attack()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						# Pause game
						self.state = 'paused'
						self.show_pause_menu()
			
			# game loop
			self.screen.fill('black')
			result = self.level.run()
			
			# Check for game over
			if result and result.get('game_over'):
				self.state = 'game_over'
				self.show_game_over()
				continue
			
			pygame.display.flip()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()