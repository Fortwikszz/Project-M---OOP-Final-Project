import pygame, sys
from code.settings import *
from code.level import *
pygame.init()


class Game:
	def __init__(self):
     
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Projeect M')
		self.clock = pygame.time.Clock()

		# level setup
		self.level = Level()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						self.level.player.attack()
			
			# game loop
			self.screen.fill('black')
			self.level.run()
			pygame.display.flip()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()