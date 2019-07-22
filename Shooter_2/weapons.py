from settings import *
from pyglet.sprite import Sprite
import random
from pyglet.gl import *

class Bullet:
    def __init__(self, x, y, rot, img, weapon, game):
        self.o_pos = Vector(x, y)
        self.pos = Vector(x, y)
        self.vector = Vector(WEAPONS[weapon]["bullet_speed"], 0).rotate(-rot)

        self.weapon = weapon

        self.sprite = Sprite(img, batch=game.bullet_batch)
        self.sprite.update(rotation=rot, scale=WEAPONS[weapon]["bullet_size"])
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2

        self.distance = 0

    def check(self, game):
        for wall in game.walls:
            if wall.pos.x + wall.width > self.pos.x > wall.pos.x and wall.pos.y + wall.height > self.pos.y > wall.pos.y:
                return True

        return False

    def update(self,dt):
        self.pos.x += self.vector.x  * dt
        self.pos.y += self.vector.y * dt

        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y

        self.distance = Vector(self.pos.x - self.o_pos.x, self.pos.y - self.o_pos.y).magnitude()

class Weapon:
    def __init__(self, weapon):
        self.name = weapon
        self.type = WEAPONS_TYPES[weapon]

        self.ammo_in_mag = WEAPONS[weapon]["ammo_clip"]
        self.extra_ammo = WEAPONS[weapon]["ammo_max"]

        self.max_ammo_in_mag = self.ammo_in_mag
        self.max_extra_ammo = self.extra_ammo

        self.fired = False

        self.spray_num = 0
    def reset(self):
        self.fired = False
        self.spray_num = 0

    def reload(self):
        if self.extra_ammo > 0 and self.ammo_in_mag != self.max_ammo_in_mag and self.fired is False:
            if self.type != "shotgun":
                a = self.max_ammo_in_mag - self.ammo_in_mag

                if self.extra_ammo - a < 0:
                    a = self.extra_ammo
                    self.extra_ammo = 0

                else:
                    self.extra_ammo -= a

                self.ammo_in_mag += a

            else:
                self.ammo_in_mag += 1
                self.extra_ammo -= 1

    def shoot(self, pos, rot, game):
        if self.ammo_in_mag > 0:
            if self.type == "auto":
                spread = WEAPONS[self.name]["spread"][self.spray_num]
                game.bullets.append(Bullet(pos.x, pos.y, rot + spread, game.bullet_img, self.name, game))
                self.spray_num += 1
                self.ammo_in_mag -= 1
                game.effects.append(MuzzleFlash(pos, rot, game))

            elif self.type == "semi-auto" and self.fired is False:
                spread = random.uniform(-WEAPONS[self.name]['spread'], WEAPONS[self.name]['spread'])
                game.bullets.append(Bullet(pos.x, pos.y, rot + spread, game.bullet_img, self.name, game))
                self.ammo_in_mag -= 1
                game.effects.append(MuzzleFlash(pos, rot, game))

            elif self.type == "shotgun" and self.fired is False:
                for a in range(WEAPONS[self.name]['bullet_count']):
                    spread = random.uniform(-WEAPONS[self.name]['spread'], WEAPONS[self.name]['spread'])
                    game.bullets.append(Bullet(pos.x, pos.y, rot + spread, game.bullet_img, self.name, game))
                self.ammo_in_mag -= 1
                game.effects.append(MuzzleFlash(pos, rot, game))

            self.fired = True

class MuzzleFlash:
    def __init__(self, pos, rot, game):
        self.pos = pos

        self.rot = rot

        self.time = 0

        self.sprite = Sprite(game.muzzle_flash_img, batch=game.effects_batch)
        self.sprite.update(rotation=rot)
        self.sprite.image.anchor_x = self.sprite.width / 3
        self.sprite.image.anchor_y = self.sprite.height / 2
        self.dead = False

        self.sprite.x = pos.x
        self.sprite.y = pos.y

    def update(self, dt):
        self.time += dt

        if self.time > MUZZLE_FLASH_LIFESPAWN:
            self.sprite.delete()
            self.dead = True

