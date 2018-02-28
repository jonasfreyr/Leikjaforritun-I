import pygame as pg
from settings import *
from tilemap import collide_hit_rect
import random
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2

            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2

            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2

            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2

            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.rot = 0

        self.last_shot = 0

        self.health = PLAYER_HEALTH

    def get_keys(self):
        self.vel = vec(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vel.x -= PLAYER_SPEED
            self.rot = 180
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
            self.rot = 0
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vel.y = PLAYER_SPEED
            self.rot = 270
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vel.y -= PLAYER_SPEED
            self.rot = 90

        if (keys[pg.K_a] or keys[pg.K_LEFT]) and (keys[pg.K_s] or keys[pg.K_DOWN]):
            self.rot = 225

        if (keys[pg.K_a] or keys[pg.K_LEFT]) and (keys[pg.K_w] or keys[pg.K_UP]):
            self.rot = 135

        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and (keys[pg.K_s] or keys[pg.K_DOWN]):
            self.rot = 315

        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and (keys[pg.K_w] or keys[pg.K_UP]):
            self.rot = 45

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel = vec(-KICKBACK).rotate(-self.rot)

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.vel = vec(ENEMY_SPEED, 0)
        self.acc = vec(8, 0)
        self.rot = 0

        self.health = ENEMY_HEALTH

        self.last_shot = 0

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))

        self.image = pg.transform.rotate(self.game.enemy_img, self.rot)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acc = vec(ENEMY_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1.5
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")

        self.rect.center = self.hit_rect.center

        now = pg.time.get_ticks()
        if now - self.last_shot > ENEMY_BULLET_RATE:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            Bullet(self.game, pos, dir)
            #self.vel = vec(-KICKBACK).rotate(-self.rot)

        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN

        elif self.health > 30:
            col = YELLOW

        else:
            col = RED

        width = int(self.rect.width * self.health / ENEMY_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < ENEMY_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.bullet_img

        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos

        spread = random.uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED

        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if (pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME) or (pg.sprite.spritecollideany(self, self.game.walls)):
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.wall_img
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE