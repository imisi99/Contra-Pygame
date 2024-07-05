import pygame
from pygame.math import Vector2 as Vector
from entity import Entity


class Player(Entity):
    def __init__(self, pos, group, path, collision_sprite, enemy_sprite, shoot):
        super().__init__(pos, group, path, shoot)

        self.collision_sprite = collision_sprite

        self.on_floor = False
        self.gravity = 15
        self.jump_speed = 1300

        self.moving_floor = None

        self.health = 10
        self.invulnerable_duration = 500

        self.enemy_sprite = enemy_sprite

        self.cooldown = 200
        self.count = 20
        self.reload_timer = 7000

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

        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = -self.jump_speed

        elif keys[pygame.K_DOWN]:
            if not self.on_floor:
                self.direction.y += 25

            else:
                self.duck = True

        else:
            self.duck = False

        if keys[pygame.K_SPACE] and self.can_shoot and self.count != 0:
            direction = Vector(1, 0) if self.status.split('_')[0] == 'right' else Vector(-1, 0)
            pos = self.rect.center + direction * 70
            y_offset = Vector(0, -10) if not self.duck else Vector(1, 10)
            self.shoot(entity=self, pos=pos + y_offset, direction=direction)

            self.can_shoot = False
            self.count -= 1
            self.shoot_time = pygame.time.get_ticks()
            self.bullet_sound.play()

        if keys[pygame.K_r] and self.shoot_time is not None:
            self.count = 0

    def get_status(self):
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + '_idle'
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + '_jump'
        if self.on_floor and self.duck:
            self.status = self.status.split('_')[0] + '_duck'

    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collision_sprite.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
                if hasattr(sprite, 'direction'):
                    self.moving_floor = sprite

    def move(self, dt):
        if self.duck and self.on_floor:
            self.direction.x = 0
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        self.enemy_collision('horizontal')

        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt

        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True

        self.rect.y = round(self.pos.y)
        self.collision('vertical')
        self.enemy_collision('vertical')
        self.moving_floor = None

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
                        self.on_floor = True
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def enemy_collision(self, direction):
        for enemy in self.enemy_sprite.sprites():
            if enemy.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.left <= enemy.rect.right and self.old_rect.left >= enemy.old_rect.right:
                        self.rect.left = enemy.rect.right
                    if self.rect.right >= enemy.rect.left and self.old_rect.right <= enemy.old_rect.left:
                        self.rect.right = enemy.rect.left
                    self.pos.x = self.rect.x

                elif direction == 'vertical':
                    if self.rect.bottom >= enemy.rect.top and self.old_rect.bottom <= enemy.old_rect.top:
                        self.rect = self.old_rect
                        self.on_floor = True
                    self.pos.x = self.old_rect.x

    def walls(self):
        if self.rect.x >= 4700:
            self.rect.x = 4700
            self.pos = self.rect
        if self.rect.x <= 390:
            self.rect.x = 390
            self.pos = self.rect
        if self.rect.y >= 2750:
            self.health = 0

    def reload(self):
        if self.count == 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.reload_timer:
                self.count = 20

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.shoot_timer()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)

        self.blink()
        self.invulnerable_timer()
        self.walls()
        self.reload()
