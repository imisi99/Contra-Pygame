import pygame
from pygame.math import Vector2 as Vector
from os import walk
from settings import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, pos, groups, path, shoot, player, collision_sprite):
        super().__init__(pos, groups, path, shoot)
        self.player = player
        for sprite in collision_sprite.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

        self.cooldown = 1000

    def get_status(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'

    def check_fire(self):
        enemy_pos = Vector(self.rect.center)
        player_pos = Vector(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 2 else False

        if distance < 500 and same_y and self.can_shoot and self.player.health > 0:
            direction = Vector(1, 0) if self.status == 'right' else Vector(-1, 0)
            pos = self.rect.center + direction * 60
            y_offset = Vector(0, -16)
            self.shoot(entity=self, pos=(pos + y_offset), direction=direction)

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.bullet_sound.play()

    def update(self, dt):
        self.get_status()
        self.animate(dt)

        self.blink()
        self.shoot_timer()
        self.check_fire()
        self.invulnerable_timer()

        self.check_death()
