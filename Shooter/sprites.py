import pygame as pg
from settings import *
from tilemap import collide_hit_rect
import random
import pytweening as tween

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
        self._layer = PLAYER_LAYER

        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        self.rot = 0

        self.last_shot = 0

        self.health = PLAYER_HEALTH

        self.weapon = "rifle"

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def draw_hit_box(self):
        hit_box = self.hit_rect.move(self.game.camera.camera.topleft)
        pg.draw.rect(self.game.screen, WHITE, hit_box, 2)

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
            self.shoot()

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now

            dir = vec(1, 0).rotate(-self.rot)

            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)

            for a in range(WEAPONS[self.weapon]['bullet_count']):
                spread = random.uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), self.rot, self.weapon)

                snd = random.choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()

                snd.play()

            MuzzleFlash(self.game, pos, self.rot, self.vel)

            self.vel = vec(-WEAPONS[self.weapon]['kickback']).rotate(-self.rot)

    def update(self):
        self.get_keys()

        self.pos += self.vel * self.game.dt

        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, weapon):
        self._layer = ENEMY_LAYER

        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.enemy_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        self.health = ENEMY_HEALTH

        self.last_shot = 0

        self.target = game.player

        self.weapon = weapon

    def draw_hit_box(self):
        hit_box = self.hit_rect.move(self.game.camera.camera.topleft)
        pg.draw.rect(self.game.screen, WHITE, hit_box, 2)

    def avoid_mobs(self):
        for enemy in self.game.enemies:
            if enemy != self:
                dist = self.pos - enemy.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS ** 2:
            self.rot = target_dist.angle_to(vec(1, 0))

            self.image = pg.transform.rotate(self.game.enemy_img, self.rot)

            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()

            if self.acc.length != 0:
                self.acc.scale_to_length(ENEMY_SPEED)

            self.acc += self.vel * -1.5

            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, "x")

            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, "y")

            self.rect.center = self.hit_rect.center


            self.shoot()


        if self.health <= 0:
            random.choice(self.game.enemy_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.blood, self.pos - vec(TILESIZE / 2, TILESIZE / 2))

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now

            dir = vec(1, 0).rotate(-self.rot)

            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)

            for a in range(WEAPONS[self.weapon]['bullet_count']):
                spread = random.uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), self.rot, self.weapon)

                snd = random.choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()

                snd.play()

            MuzzleFlash(self.game, pos, self.rot, self.vel)

            #self.vel = vec(-WEAPONS[self.weapon]['kickback']).rotate(-self.rot)

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
    def __init__(self, game, pos, dir, angle, weapon):
        self._layer = BULLET_LAYER

        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rot = angle

        self.image = game.bullet_images[WEAPONS[weapon]['bullet_size']]
        self.image = pg.transform.rotate(self.image, self.rot)

        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos

        #spread = random.uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed']

        self.spawn_time = pg.time.get_ticks()

        self.weapon = weapon

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if (pg.time.get_ticks() - self.spawn_time > WEAPONS[self.weapon]['bullet_lifetime']) or (pg.sprite.spritecollideany(self, self.game.walls)):
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER

        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.wall_img
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = WALL_LAYER

        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rect = pg.Rect(x, y, w, h)

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos, rot, vel):
        self._layer = EFFECTS_LAYER

        self.groups = game.all_sprites
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        size = random.randint(20, 50)

        self.image = pg.transform.scale(game.gun_flash, (size * 2, size))
        self.image = pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()

        self.pos = pos
        self.rect.center = pos

        self.vel = vel

        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

        self.rect.center += self.vel * self.game.dt

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER

        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.item_images[type]
        self.image = pg.transform.scale(self.image, ITEM_SIZES[type])
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.pos = pos

        self.type = type

        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)

        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED

        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1