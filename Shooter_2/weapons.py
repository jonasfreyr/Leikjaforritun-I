from settings import *
from pyglet.sprite import Sprite
import random
from pyglet.gl import *

class Bullet:
    def __init__(self, x, y, rot, img, weapon, game, main=True):
        self.o_pos = Vector(x, y)
        self.pos = Vector(x, y)
        self.vector = Vector(WEAPONS[weapon]["bullet_speed"], 0).rotate(-rot)

        self.weapon = weapon

        self.sprite = Sprite(img, batch=game.bullet_batch)
        self.sprite.update(rotation=rot, scale=WEAPONS[weapon]["bullet_size"])
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2

        self.distance = 0

        if main:
            game.o_bullets.append({"rot": rot, "pos": {"x": x, "y": y}, "weapon": weapon})

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

        self.recovery_time = 0

    def reset(self):
        self.fired = False

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
                if self.spray_num > len(WEAPONS[self.name]["spread"]) - 1:
                    self.spray_num = 0

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

    def update(self, dt):
        if self.type == "auto":
            if self.recovery_time >= WEAPONS[self.name]["recovery_time"]:
                self.spray_num = 0
                self.recovery_time = 0

            else:
                self.recovery_time += dt

class Animation(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.deleted = False

    def on_animation_end(self):
        self.delete()
        self.deleted = True

class Grenade:
    def __init__(self, game, type):
        self.game = game

        self.type = type

        self.explode = False

        self.tossed = False

        self.duration = 0
        self.opacity = 255

    def throw(self, pos, vel, rot, o=False):
        self.pos = pos
        self.vel = vel.rotate(-rot)
        self.slow = GRENADE_SLOWDOWN.copy().rotate(-rot)

        if self.type == "grenade":
            self.sprite = Sprite(self.game.granade_img, pos.x, pos.y, batch=self.game.main_batch)

        elif self.type == "smoke":
            self.sprite = Sprite(self.game.smoke_img, pos.x, pos.y, batch=self.game.main_batch)

        self.sprite.image.anchor_x = self.sprite.width / 2
        self.sprite.image.anchor_y = self.sprite.height / 2

        self.explode_sprite = None

        self.hit_box = GRENADE_HIT_BOX.copy()
        self.hit_box.x = pos.x - self.hit_box.width / 2
        self.hit_box.y = pos.y - self.hit_box.height / 2

        self.tossed = True

        self.game.grenades.append(self)

        if o is False:
            self.game.o_grenades.append({"pos": {"x": pos.x, "y": pos.y}, "vel": {"x": vel.x, "y": vel.y}, "rot": rot, "type": self.type})

    def collide_with_walls(self, dir):
        if dir == "x":
            for wall in self.game.walls:
                if (self.hit_box.x + self.hit_box.width > wall.pos.x and self.hit_box.y + self.hit_box.height > wall.pos.y) and (self.hit_box.x < wall.pos.x + wall.width and self.hit_box.y < wall.pos.y + wall.height):
                    if wall.center.x > self.hit_box.get_center().x:
                        self.hit_box.x = wall.pos.x - self.hit_box.width

                    elif wall.center.x < self.hit_box.get_center().x:
                        self.hit_box.x = wall.pos.x + wall.width

                    self.vel.x = -self.vel.x
                    self.slow.x = -self.slow.x

        elif dir == "y":
            for wall in self.game.walls:
                if (self.hit_box.x + self.hit_box.width > wall.pos.x and self.hit_box.y + self.hit_box.height > wall.pos.y) and (self.hit_box.x < wall.pos.x + wall.width and self.hit_box.y < wall.pos.y + wall.height):
                    if wall.center.y > self.hit_box.get_center().y:
                        self.hit_box.y = wall.pos.y - self.hit_box.height

                    elif wall.center.y < self.hit_box.get_center().y:
                        self.hit_box.y = wall.pos.y + wall.height

                    self.vel.y = -self.vel.y
                    self.slow.y = -self.slow.y

    def draw_hit_box(self):
        glBegin(GL_LINES)

        glVertex2i(int(self.hit_box.x), int(self.hit_box.y))
        glVertex2i(int(self.hit_box.x), int(self.hit_box.y + self.hit_box.height))

        glVertex2i(int(self.hit_box.x), int(self.hit_box.y + self.hit_box.height))
        glVertex2i(int(self.hit_box.x + self.hit_box.width), int(self.hit_box.y + self.hit_box.height))

        glVertex2i(int(self.hit_box.x + self.hit_box.width), int(self.hit_box.y + self.hit_box.height))
        glVertex2i(int(self.hit_box.x + self.hit_box.width), int(self.hit_box.y))

        glVertex2i(int(self.hit_box.x + self.hit_box.width), int(self.hit_box.y))
        glVertex2i(int(self.hit_box.x), int(self.hit_box.y))

        glEnd()

    def update(self, dt):
        if not self.vel.magnitude() <= 4 and self.tossed:
            self.vel.x -= self.slow.x * dt
            self.vel.y -= self.slow.y * dt

            # check hit box collisions
            self.hit_box.x += self.vel.x * dt
            self.collide_with_walls("x")

            self.hit_box.y += self.vel.y * dt
            self.collide_with_walls("y")

            self.pos.x = self.hit_box.x + self.hit_box.width / 2
            self.pos.y = self.hit_box.y + self.hit_box.height / 2

            self.sprite.x = self.pos.x
            self.sprite.y = self.pos.y

        else:
            if self.explode is False:
                self.sprite.delete()

                self.vel.multiply(0)
                self.explode = True
                if self.type == "grenade":
                    self.explode_sprite = Animation(self.game.explosion_anim, self.pos.x, self.pos.y, batch=self.game.effects_batch)

                elif self.type == "smoke":
                    self.explode_sprite = Animation(self.game.smoke, self.pos.x, self.pos.y, batch=self.game.effects_batch)

                    self.duration = SMOKE_DURATION

                self.explode_sprite.x = self.pos.x - self.explode_sprite.width / 2
                self.explode_sprite.y = self.pos.y - self.explode_sprite.height / 2

        if self.type == "smoke" and self.explode is True:
            if self.duration <= 0:
                if self.opacity <= 0:
                    self.explode_sprite.deleted = True

                self.explode_sprite.opacity = self.opacity
                if self.opacity > 0:
                    self.opacity -= int(300 * dt)

            else:
                self.duration -= dt


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

