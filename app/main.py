import sys
import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from pygame.math import Vector2 as Vector
from bullet import Bullet, FireAnimation
from enemy import Enemy


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector()

        self.fg_sky = pygame.image.load('../graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('../graphics/sky/bg_sky.png').convert_alpha()
        map_tmx = load_pygame('../data/map.tmx')

        self.padding = WINDOW_WIDTH / 2
        self.sky_width = self.fg_sky.get_width()
        self.map_width = map_tmx.tilewidth * map_tmx.width + (2 * self.padding)
        self.sky_num = self.map_width // self.sky_width

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for x in range(int(self.sky_num)):
            x_pos = -self.padding + (x * self.sky_width)
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2.5, 850 - self.offset.y / 2.5))
            self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2, 850 - self.offset.y / 2))

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
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
        self.bullet_sprite = pygame.sprite.Group()

        pygame.display.set_caption('Contra')
        self.setup()

        self.bullet_surf = pygame.image.load('../graphics/bullet.png').convert_alpha()
        self.fire_surf = [pygame.image.load('../graphics/fire/0.png').convert_alpha(),
                          pygame.image.load('../graphics/fire/1.png').convert_alpha()]

    def setup(self):
        tmx_map = load_pygame('../data/map.tmx')
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * 64, y * 64), surf, [self.all_sprites, self.collision_sprite])

        for layers in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layers).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, LAYERS[layers])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, '../graphics/player', self.collision_sprite,
                                     self.shoot)
            if obj.name == 'Enemy':
                Enemy((obj.x, obj.y), self.all_sprites, '../graphics/enemies', self.shoot, self.player, self.collision_sprite)

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
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def bullet_collision(self):
        for bullet in self.bullet_sprite.sprites():
            if pygame.sprite.spritecollide(bullet, self.collision_sprite, False):
                bullet.kill()

    def shoot(self, pos, direction, entity):
        Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprite])
        FireAnimation(entity, self.fire_surf, direction, [self.all_sprites])

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

            self.bullet_collision()

            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == '__main__':
    game = Begin()
    game.run()
