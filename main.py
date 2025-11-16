import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Piton PBO FP Main")

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)