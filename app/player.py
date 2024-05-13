import pygame
from pygame.math import Vector2 as Vector
from settings import *
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, path, collision_sprite):
        super().__init__(group)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'right_idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['Level']
        self.collision_sprite = collision_sprite

        self.direction = Vector()
        self.pos = Vector(self.rect.topleft)

        self.speed = 200
        self.old_rect = self.rect.copy()

    def import_assets(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []

            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -5
            if self.status == 'left_duck':
                self.status == 'left_idle'
            elif self.status == 'left':
                self.status == 'left_jump'
            elif self.status == 'right':
                self.status == 'left_jump'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            if self.status == 'left':
                self.status = 'left_duck'
            elif self.status == 'right':
                self.status = 'right_duck'
        else:
            self.direction.y = 0

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprite.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x

                elif direction == 'vertical':
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y

    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.animate(dt)
