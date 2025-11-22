import pygame, sys
from settings import *
from main_mape import *
from main_awi import *
pygame.init()


class Game:
	def __init__(self):
     
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_caption('Projeect M')
		self.clock = pygame.time.Clock()

		# level setup
		self.main_mape = Level()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			
			# game loop
			self.screen.fill('black')
			self.main_mape.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()