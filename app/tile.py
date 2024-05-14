import pygame
from settings import *
from pygame.math import Vector2 as Vector


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, level):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = level


class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups, LAYERS['Level'])
        self.old_rect = self.rect.copy()


class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.direction = Vector(0, -1)
        self.pos = Vector(self.rect.topleft)
        self.speed = 200

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

