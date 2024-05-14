import sys
import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from pygame.math import Vector2 as Vector


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for sprite in sorted(self.sprites(), key=lambda sprite : sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Begin:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprites()
        self.collision_sprite = pygame.sprite.Group()
        self.platform_sprite = pygame.sprite.Group()

        pygame.display.set_caption('Contra')
        self.setup()

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprite])

        for layers in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layers).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, LAYERS[layers])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, '../graphics/player', self.collision_sprite)

        self.platform_border = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprite,
                                                           self.platform_sprite])
            else:
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border.append(border_rect)

    def platform_collision(self):
        for platform in self.platform_sprite.sprites():
            for border in self.platform_border:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(120) / 1000
            self.display_surface.fill((249, 131, 103))

            self.platform_collision()
            self.all_sprites.update(dt)

            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == '__main__':
    game = Begin()
    game.run()
