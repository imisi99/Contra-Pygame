import sys
import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile
from player import Player
from pygame.math import Vector2 as Vector


class AllSprite(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Begin:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprite()

        pygame.display.set_caption('Contra')
        self.setup()

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            Tile((x * 64, y * 64), surf, self.all_sprites)
        self.player = Player((200, 300), self.all_sprites)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(120) / 1000
            self.display_surface.fill((249, 131, 103))

            self.all_sprites.update(dt)

            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == '__main__':
    game = Begin()
    game.run()
