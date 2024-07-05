import pygame
from settings import *


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


class EnemyNum:
    def __init__(self, enemy):
        self.enemies = enemy
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../graphics/subatomic.ttf', 20)

    def display(self):
        text = f'Enemies: {len(self.enemies)}'
        display = self.font.render(text, True, 'blue')
        display_rect = display.get_rect(center=(WINDOW_WIDTH - 100, 30))
        pygame.draw.rect(self.display_surface, 'red', display_rect.inflate(30, 30), width=5, border_radius=10)
        self.display_surface.blit(display, display_rect)


class BulletCount:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../graphics/subatomic.ttf', 20)

    def display(self):
        if self.player.count != 0:
            text = f'Bullet: {self.player.count}'
        else:
            text = 'Reloading...'
        display = self.font.render(text, True, 'blue')
        display_rect = display.get_rect(center=(WINDOW_WIDTH - 100, 80))
        pygame.draw.rect(self.display_surface, 'red', display_rect.inflate(30, 30), width=5, border_radius=10)
        self.display_surface.blit(display, display_rect)
