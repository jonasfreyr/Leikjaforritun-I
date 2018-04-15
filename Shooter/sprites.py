import pygame as pg
from settings import *
from tilemap import collide_hit_rect
import random, math
import pytweening as tween
from hud import *


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

        self.weapon = "pistol"

        self.image = game.player_images[self.weapon]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        self.rot = 0

        self.last_shot = 0

        self.health = PLAYER_HEALTH
        self.armor = 0

        self.ammo = WEAPONS[self.weapon]['ammo_clip']
        self.maxammo = WEAPONS[self.weapon]['ammo_max']

        self.cursor = self.game.crosshair_img
        self.cursor_rect = self.cursor.get_rect()

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def reload(self):
        self.game.effects_sounds['reload'].play()

        if WEAPON_TYPES[self.weapon] != 'shotgun':
            a = WEAPONS[self.weapon]['ammo_clip'] - self.ammo

            if self.maxammo - a < 0:
                a = self.maxammo
                self.maxammo = 0
            else:
                self.maxammo -= a

            self.ammo += a

        else:
            self.ammo += 1
            self.maxammo -= 1

    def draw_hit_box(self):
        hit_box = self.hit_rect.move(self.game.camera.camera.topleft)
        pg.draw.rect(self.game.screen, WHITE, hit_box, 2)

    def get_mouse(self):
        posM = pg.mouse.get_pos()

        self.cursor_rect.center = posM

        self.cursor_rect = self.game.camera.apply_mouse_rect(self.cursor_rect)

        v = self.pos - self.cursor_rect.center

        self.rot = v.angle_to(vec(-1, 0))

    def get_keys(self):
        self.vel = vec(0, 0)

        mouse = pg.mouse.get_pressed()

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x -= PLAYER_SPEED

        if keys[pg.K_d]:
            self.vel.x += PLAYER_SPEED

        if keys[pg.K_s]:
            self.vel.y += PLAYER_SPEED

        if keys[pg.K_w]:
            self.vel.y -= PLAYER_SPEED

        if keys[pg.K_TAB]:
            self.game.tab = True

        self.get_mouse()

        if mouse[0] == 1:
            if self.ammo != 0:
                self.shoot()

            else:
                now = pg.time.get_ticks()
                if now - self.last_shot > WEAPONS[self.weapon]['rate']:
                    self.last_shot = now
                    self.game.out_ammo.play()

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.ammo -= 1

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

        self.image = pg.transform.rotate(self.game.player_images[self.weapon], self.rot)
        self.rect = self.image.get_rect()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.windows, 'x')

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.windows, 'y')

        self.rect.center = self.hit_rect.center


class Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER

        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

    def draw_hit_box(self):
        hit_box = self.hit_rect.move(self.game.camera.camera.topleft)
        pg.draw.rect(self.game.screen, WHITE, hit_box, 2)


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, weapon, last_known=None):
        self._layer = ENEMY_LAYER

        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.enemy_images[weapon].copy()
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

        if last_known is None:
            self.moving = False
            self.last_known = [int(self.pos.x), int(self.pos.y)]

        else:
            self.moving = True
            self.last_known = last_known

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

    def lineLine(self, x1, y1, x2, y2, x3, y3, x4, y4):

        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

        if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True

        else:
            return False

    def line_collide(self,):
        target_dist = self.target.pos - self.pos
        rot = target_dist.angle_to(vec(1, 0))
        pos = self.pos + BARREL_OFFSET.rotate(-rot)

        for a in self.game.walls:
            r = a.rect.copy()
            topleft = r.topleft
            topright = r.topright

            bottomleft = r.bottomleft
            bottomright = r.bottomright

            left = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topleft[0], bottomleft[1])

            right = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topright[0], topright[1], topright[0], bottomright[1])

            top = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        for a in self.game.enemies:
            r = a.hit_rect.copy()
            topleft = r.topleft
            topright = r.topright

            bottomleft = r.bottomleft
            bottomright = r.bottomright

            left = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topleft[0],
                                 bottomleft[1])

            right = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topright[0], topright[1],
                                  topright[0], bottomright[1])

            top = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topright[0],
                                topright[1])

            bottom = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, bottomleft[0], bottomleft[1],
                                   bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def rot_towards_target(self, target_dist):
        rotT = target_dist.angle_to(vec(1, 0))

        angle = math.atan2(-target_dist.x, -target_dist.y)/math.pi * 180.0

        diff = (angle - self.rot - 90) % 360

        if 175 < int(diff) < 183:
            rot = rotT

        elif diff > 180:
            rot = self.rot + ENEMY_ROTATION_SPEED

        else:
            rot = self.rot - ENEMY_ROTATION_SPEED

        return rot

    def move(self):
        target_dist = self.last_known - self.pos
        self.rot = self.rot_towards_target(target_dist)
        # self.rot = target_dist.angle_to(vec(1, 0))

        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()

        try:
            self.acc.scale_to_length(ENEMY_SPEED)

        except:
            pass

        self.acc += self.vel * -1.5

        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        collide_with_walls(self, self.game.windows, "x")

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        collide_with_walls(self, self.game.windows, "y")

        self.rect.center = self.hit_rect.center

    def update(self):
        self.target = self.game.player
        closest = self.target.pos - self.pos
        for a in self.game.ally:
            target_dist = a.pos - self.pos

            if target_dist.length() < closest.length():
                closest = target_dist
                self.target = a

        target_dist = closest
        if target_dist.length_squared() < (WEAPONS[self.weapon]['detect_radius'] - NIGHT_RADIUS) ** 2:
            if self.line_collide() is False:
                self.moving = False

                self.vel = vec(0, 0)

                self.last_known = [int(self.target.pos.x), int(self.target.pos.y)]

                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                target_distA = self.target.pos - pos

                self.rot = self.rot_towards_target(target_distA)

                self.image = pg.transform.rotate(self.game.enemy_images[self.weapon], self.rot)

                self.rect = self.image.get_rect()
                self.rect.center = self.pos

                rot = target_dist.angle_to(vec(1, 0))

                if self.rot - 20 < rot < self.rot + 20:
                    self.shoot()

            else:
                self.moving = True
                self.image = pg.transform.rotate(self.game.enemy_images[self.weapon], self.rot)
        else:
            self.moving = True
            self.image = pg.transform.rotate(self.game.enemy_images[self.weapon], self.rot)

        pos = [int(self.pos.x), int(self.pos.y)]

        if ((pos[0] - 5 < self.last_known[0]) and (pos[1] - 5 < self.last_known[1])) and ((pos[0] + 5 > self.last_known[0]) and (pos[1] + 5 > self.last_known[1])):
            self.moving = False

        if self.moving:
            self.move()

        if self.health <= 0:
            random.choice(self.game.enemy_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.blood, self.pos - vec(TILESIZE / 2, TILESIZE / 2))
            self.game.kills += 1

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


class Ally(pg.sprite.Sprite):
    def __init__(self, game, x, y, weapon, last_known=None):
        self._layer = ENEMY_LAYER

        self.groups = game.all_sprites, game.ally
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.player_images[weapon].copy()
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

        self.target = game.enemies

        if last_known is None:
            self.moving = False
            self.last_known = [int(self.pos.x), int(self.pos.y)]

        else:
            self.moving = True
            self.last_known = last_known

        self.weapon = weapon
        self.selected = False

    def draw_hit_box(self):
        hit_box = self.hit_rect.move(self.game.camera.camera.topleft)
        pg.draw.rect(self.game.screen, WHITE, hit_box, 2)

    def avoid_mobs(self):
        for enemy in self.game.enemies:
            if enemy != self:
                dist = self.pos - enemy.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def lineLine(self, x1, y1, x2, y2, x3, y3, x4, y4):

        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

        if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True

        else:
            return False

    def line_collide(self,):
        target_dist = self.target.pos - self.pos
        rot = target_dist.angle_to(vec(1, 0))
        pos = self.pos + BARREL_OFFSET.rotate(-rot)

        for a in self.game.walls:
            r = a.rect.copy()
            topleft = r.topleft
            topright = r.topright

            bottomleft = r.bottomleft
            bottomright = r.bottomright

            left = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topleft[0], bottomleft[1])

            right = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topright[0], topright[1], topright[0], bottomright[1])

            top = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        for a in self.game.ally:
            r = a.hit_rect.copy()
            topleft = r.topleft
            topright = r.topright

            bottomleft = r.bottomleft
            bottomright = r.bottomright

            left = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topleft[0],
                                 bottomleft[1])

            right = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topright[0], topright[1],
                                  topright[0], bottomright[1])

            top = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, topleft[0], topleft[1], topright[0],
                                topright[1])

            bottom = self.lineLine(pos.x, pos.y, self.target.pos.x, self.target.pos.y, bottomleft[0], bottomleft[1],
                                   bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def rot_towards_target(self, target_dist):
        rotT = target_dist.angle_to(vec(1, 0))

        angle = math.atan2(-target_dist.x, -target_dist.y)/math.pi * 180.0

        diff = (angle - self.rot - 90) % 360

        if 175 < int(diff) < 183:
            rot = rotT

        elif diff > 180:
            rot = self.rot + ENEMY_ROTATION_SPEED

        else:
            rot = self.rot - ENEMY_ROTATION_SPEED

        return rot

    def update(self):
        closest = vec(9999, 9999)
        for a in self.game.enemies:
            target_dist = a.pos - self.pos

            if target_dist.length() < closest.length():
                closest = target_dist
                self.target = a

        if closest.length_squared() < (WEAPONS[self.weapon]['detect_radius'] - NIGHT_RADIUS) ** 2:
            if self.line_collide() is False:
                self.moving = False

                self.vel = vec(0, 0)

                self.last_known = [int(self.target.pos.x), int(self.target.pos.y)]

                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                target_distA = self.target.pos - pos

                self.rot = self.rot_towards_target(target_distA)

                self.image = pg.transform.rotate(self.game.player_images[self.weapon], self.rot)

                self.rect = self.image.get_rect()
                self.rect.center = self.pos

                rot = closest.angle_to(vec(1, 0))

                if self.rot - 20 < rot < self.rot + 20:
                    self.shoot()

            else:
                self.moving = True
                self.image = pg.transform.rotate(self.game.player_images[self.weapon], self.rot)
        else:
            self.moving = True
            self.image = pg.transform.rotate(self.game.player_images[self.weapon], self.rot)

        pos = [int(self.pos.x), int(self.pos.y)]

        if ((pos[0] - 5 < self.last_known[0]) and (pos[1] - 5 < self.last_known[1])) and ((pos[0] + 5 > self.last_known[0]) and (pos[1] + 5 > self.last_known[1])):
            self.moving = False

        self.moving = False
        if self.moving:
            target_dist = self.last_known - self.pos
            self.rot = self.rot_towards_target(target_dist)
            #self.rot = target_dist.angle_to(vec(1, 0))

            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()

            try:
                self.acc.scale_to_length(ENEMY_SPEED)

            except:
                pass

            self.acc += self.vel * -1.5

            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, "x")
            collide_with_walls(self, self.game.windows, "x")

            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, "y")
            collide_with_walls(self, self.game.windows, "y")

            self.rect.center = self.hit_rect.center

        if self.health <= 0:
            random.choice(self.game.enemy_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.blood, self.pos - vec(TILESIZE / 2, TILESIZE / 2))
            self.game.deaths += 1

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
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * random.uniform(0.9, 1.1)

        self.spawn_time = pg.time.get_ticks()

        self.weapon = weapon

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if (pg.time.get_ticks() - self.spawn_time > WEAPONS[self.weapon]['bullet_lifetime']) or (pg.sprite.spritecollideany(self, self.game.walls)):
            self.kill()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, type):
        self._layer = WALL_LAYER

        if type == "Wall":
            self.groups = game.walls

        elif type == "Window":
            self.groups = game.windows

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