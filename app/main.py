import sys
import pygame
from settings import *


class Begin:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Contra')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(120) / 1000
            self.display_surface.fill((249, 131, 103))

            pygame.display.update()


if __name__ == '__main__':
    game = Begin()
    game.run()
