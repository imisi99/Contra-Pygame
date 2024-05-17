import pygame
from settings import *
from pygame.math import Vector2 as Vector


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(groups)
        self.image = surf
        if direction.x < 0:
            self.image = pygame.transform.flip(surf, True, False)
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['Level']

        self.direction = direction
        self.pos = Vector(self.rect.center)
        self.speed = 750

        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if pygame.time.get_ticks() - self.start_time > 1000:
            self.kill()


class FireAnimation(pygame.sprite.Sprite):
    def __init__(self, entity, surf_list, direction, groups):
        super().__init__(groups)
        self.entity = entity

        self.frames = surf_list
        if direction.x < 0:
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]

        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.z = LAYERS['Level']

        x_offset = 60 if direction.x > 0 else -60
        y_offset = 10 if entity.duck else -10
        self.offset = Vector(x_offset, y_offset)

        self.rect = self.image.get_rect(center=self.entity.rect.center + self.offset)

    def animate(self, dt):
        self.frames_index += 15 * dt
        if self.frames_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frames_index)]

    def move(self):
        self.rect.center = self.entity.rect.center + self.offset

    def update(self, dt):
        self.animate(dt)
        self.move()
