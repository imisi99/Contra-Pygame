import pygame


class HealthBar:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('../graphics/health.png').convert_alpha()

    def display(self):
        for x in range(self.player.health):
            x = x * (self.image.get_width() + 2)
            y = 10
            self.display_surface.blit(self.image, (x, y))

