import pyglet
from vector import Vector
from settings import *
from pyglet.gl import *
from pyglet.sprite import Sprite
# import pygame as pg
import math
from weapons import *

class Oplayers:
    def __init__(self, id, pos, rot, weapon, game):
        self.id = id

        self.pos = pos

        self.rot = rot

        self.weapon = weapon

        self.sprite = Sprite(game.player_images[weapon])
        self.width = self.sprite.width
        self.height = self.sprite.height

        self.hit_box = PLAYER_HIT_BOX.copy()
        self.hit_box.x = pos.x
        self.hit_box.y = pos.y

        self.sprite.image.anchor_x = self.sprite.image.width / 2 - WEAPONS[weapon]['img_offset'].x
        self.sprite.image.anchor_y = self.sprite.image.height / 2 - WEAPONS[weapon]['img_offset'].y

        self.game = game

        self.health = PLAYER_HEALTH
        self.dead = False

    def update(self):
        self.sprite = Sprite(self.game.player_images[self.weapon])
        self.width = self.sprite.width
        self.height = self.sprite.height

        self.sprite.image.anchor_x = self.sprite.image.width / 2 - WEAPONS[self.weapon]['img_offset'].x
        self.sprite.image.anchor_y = self.sprite.image.height / 2 - WEAPONS[self.weapon]['img_offset'].y

        self.sprite.update(rotation=self.rot)

        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y

        self.hit_box.x = self.pos.x - self.hit_box.width / 2
        self.hit_box.y = self.pos.y - self.hit_box.height / 2

        # print(self.pos)

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

class Mob:
    def __init__(self, x, y, game):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)

        self.game = game

        self.rot = 0

        self.hit_box = MOB_HIT_BOX.copy()

        self.sprite = Sprite(game.mob_image, batch=game.mob_batch)
        self.width = self.sprite.width
        self.height = self.sprite.height

        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2

        self.sprite.x = x
        self.sprite.y = y

        self.health = MOB_HEALTH

        self.hit_box.x = self.pos.x - self.hit_box.width / 2
        self.hit_box.y = self.pos.y - self.hit_box.height / 2

        self.target = None

    def collide_with_walls(self, dir):
        if self.health > 0:
            if dir == "x":
                for wall in self.game.walls:
                    if (self.hit_box.x + self.hit_box.width > wall.pos.x and self.hit_box.y + self.hit_box.height > wall.pos.y) and (self.hit_box.x < wall.pos.x + wall.width and self.hit_box.y < wall.pos.y + wall.height):
                        if wall.center.x > self.hit_box.get_center().x:
                            self.hit_box.x = wall.pos.x - self.hit_box.width

                        elif wall.center.x < self.hit_box.get_center().x:
                            self.hit_box.x = wall.pos.x + wall.width

                        self.vel.x = 0

            elif dir == "y":
                for wall in self.game.walls:
                    if (self.hit_box.x + self.hit_box.width > wall.pos.x and self.hit_box.y + self.hit_box.height > wall.pos.y) and (self.hit_box.x < wall.pos.x + wall.width and self.hit_box.y < wall.pos.y + wall.height):
                        if wall.center.y > self.hit_box.get_center().y:
                            self.hit_box.y = wall.pos.y - self.hit_box.height

                        elif wall.center.y < self.hit_box.get_center().y:
                            self.hit_box.y = wall.pos.y + wall.height

                        self.vel.y = 0

    def rot_towards_target(self, target_dist):
        rotT = target_dist.get_angle() - 90

        angle = math.atan2(-target_dist.x, -target_dist.y)/math.pi * 180.0

        diff = (angle - self.rot - 90) % 360

        if 175 < int(diff) < 183:
            rot = rotT

        elif diff > 180:
            rot = self.rot + MOB_ROTATION_SPEED

        else:
            rot = self.rot - MOB_ROTATION_SPEED

        return rot

    def move(self):
        dist = self.target - self.pos

    def update(self, dt):
        dist = None
        for player in self.game.o_players:
            new_dist = player.pos - self.pos

            if dist is None:
                dist = new_dist

            elif new_dist.magnitude() < dist.magnitude():
                dist = new_dist

        if dist is not None:
            self.rot = self.rot_towards_target(dist)

        self.hit_box.x += self.vel.x * dt
        self.collide_with_walls("x")

        self.hit_box.y += self.vel.y * dt
        self.collide_with_walls("y")

        self.pos.x = self.hit_box.x + self.hit_box.width / 2
        self.pos.y = self.hit_box.y + self.hit_box.height / 2

        self.sprite.update(rotation=self.rot)
        self.sprite.x = self.hit_box.get_center().x
        self.sprite.y = self.hit_box.get_center().y

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

class Player:
    def __init__(self, x, y, game, weapon):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)

        self.rot = 0

        self.game = game

        self.weapons = [None, Weapon("pistol")]

        self.grenades = [Grenade(self.game, "smoke"),Grenade(self.game, "grenade"),Grenade(self.game, "smoke"),Grenade(self.game, "grenade"),Grenade(self.game, "smoke")]
        self.grenade_num = 0

        self.last_shot = 0

        self.hit_box = PLAYER_HIT_BOX.copy()
        self.hit_box.x = x
        self.hit_box.y = y

        self.o = Vector(self.pos.x, self.pos.y)

        self.health = PLAYER_HEALTH

        self.num = 1

        self.sprite = Sprite(game.player_images[self.weapons[self.num].name])
        self.width = self.sprite.width
        self.height = self.sprite.height

        self.sprite.image.anchor_x = self.sprite.image.width / 2 - WEAPONS[self.weapons[self.num].name]['img_offset'].x
        self.sprite.image.anchor_y = self.sprite.image.height / 2 - WEAPONS[self.weapons[self.num].name]['img_offset'].y

        self.knock_back = Vector(0, 0)

    def see_player(self, player):
        corner2 = Vector(self.hit_box.x + self.hit_box.width / 2, self.hit_box.y + self.hit_box.height / 2)

        return self.see_point(player, corner2)

    def see_point(self, player, point_1):
        o_point_1 = player.hit_box.copy()
        o_point_2 = Vector(player.hit_box.x, player.hit_box.y + player.hit_box.height)
        o_point_3 = Vector(player.hit_box.x + player.hit_box.width, player.hit_box.y + player.hit_box.height)
        o_point_4 = Vector(player.hit_box.x + player.hit_box.width, player.hit_box.y)

        glBegin(GL_LINES)
        glVertex2i(int(point_1.x), int(point_1.y))
        glVertex2i(int(o_point_1.x), int(o_point_1.y))
        glEnd()

        glBegin(GL_LINES)
        glVertex2i(int(point_1.x), int(point_1.y))
        glVertex2i(int(o_point_2.x), int(o_point_2.y))
        glEnd()

        glBegin(GL_LINES)
        glVertex2i(int(point_1.x), int(point_1.y))
        glVertex2i(int(o_point_3.x), int(o_point_3.y))
        glEnd()

        glBegin(GL_LINES)
        glVertex2i(int(point_1.x), int(point_1.y))
        glVertex2i(int(o_point_4.x), int(o_point_4.y))
        glEnd()

        if self.line_collide(self.game, point_1, o_point_1) and self.line_collide(self.game, point_1, o_point_2) and self.line_collide(self.game, point_1, o_point_3) \
            and self.line_collide(self.game, point_1, o_point_4):
            return False

        return True

    def line_collide(self, game, pos, o):
        for wall in game.walls:
            topleft = [wall.pos.x, wall.pos.y + wall.height]
            topright = [wall.pos.x + wall.width, wall.pos.y + wall.height]

            bottomleft = [wall.pos.x, wall.pos.y]
            bottomright = [wall.pos.x + wall.width, wall.pos.y]

            left = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topleft[0], bottomleft[1])

            right = lineLine(pos.x, pos.y, o.x, o.y, topright[0], topright[1], topright[0], bottomright[1])

            top = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = lineLine(pos.x, pos.y, o.x, o.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def switch(self):

        self.num += 1

        if len(self.weapons)-1 < self.num:
            self.num = 0

        if self.weapons[self.num] is None:
            self.switch()

    def get_rotation(self, point1, point2):
        return math.degrees(math.atan2(point1.x - point2.x, point1.y - point2.y))

    def throw(self, dt):
        if len(self.grenades) > 0:
            self.grenades[self.grenade_num].throw(Vector(self.pos.x, self.pos.y), GRENADE_STARTING_VEL + self.vel * Vector(dt, dt), self.rot)
            self.grenades.remove(self.grenades[self.grenade_num])

            self.grenade_num = 0

    def shoot(self):
        if self.last_shot <= 0 < self.health:
            rot = self.get_rotation(self.o, self.game.mouse.get_map_pos()) + 90

            if abs(self.rot) - abs(rot) > 10 or abs(rot) - abs(self.rot) > 10:
                rot = self.rot

            if self.weapons[self.num].ammo_in_mag > 0 and not self.weapons[self.num].fired:
                self.knock_back = WEAPONS[self.weapons[self.num].name]["knock_back"].rotate(self.rot)

            self.weapons[self.num].shoot(self.o, self.pos, rot, self.game)

            self.last_shot = WEAPONS[self.weapons[self.num].name]["rate"]

    def rotate_to_mouse(self):
        '''
        v = self.pos - self.game.mouse.get_map_pos()


        s = self.game.mouse.get_map_pos()
        pos = pg.Vector2(self.pos.x, self.pos.y)
        pos2 = pg.Vector2(s.x, s.y)

        v2 = pos - pos2


        print("v: ", v)
        print("v2: ", v2)


        # print(v.angle_to(Vector(-1, 0)))
        # print(v2.angle_to(pg.Vector2(-1, 0)))

        # print(self.rot)

        print(v.magnitude())
        print(v2.magnitude())
        '''

        self.rot = self.get_rotation(self.pos, self.game.mouse.get_map_pos()) + 90

    def collide_with_walls(self, dir):
        if self.health > 0:
            if dir == "x":
                for wall in self.game.walls:
                    if (self.hit_box.x + self.hit_box.width > wall.pos.x and self.hit_box.y + self.hit_box.height > wall.pos.y) and (self.hit_box.x < wall.pos.x + wall.width and self.hit_box.y < wall.pos.y + wall.height):
                        if wall.center.x > self.hit_box.get_center().x:
                            self.hit_box.x = wall.pos.x - self.hit_box.width

                        elif wall.center.x < self.hit_box.get_center().x:
                            self.hit_box.x = wall.pos.x + wall.width

                        self.vel.x = 0

            elif dir == "y":
                for wall in self.game.walls:
                    if (self.hit_box.x + self.hit_box.width > wall.pos.x and self.hit_box.y + self.hit_box.height > wall.pos.y) and (self.hit_box.x < wall.pos.x + wall.width and self.hit_box.y < wall.pos.y + wall.height):
                        if wall.center.y > self.hit_box.get_center().y:
                            self.hit_box.y = wall.pos.y - self.hit_box.height

                        elif wall.center.y < self.hit_box.get_center().y:
                            self.hit_box.y = wall.pos.y + wall.height

                        self.vel.y = 0

    def update(self, dt, server=False):
        self.sprite = Sprite(self.game.player_images[self.weapons[self.num].name])
        self.width = self.sprite.width
        self.height = self.sprite.height

        self.sprite.image.anchor_x = self.sprite.image.width / 2 - WEAPONS[self.weapons[self.num].name]['img_offset'].x
        self.sprite.image.anchor_y = self.sprite.image.height / 2 - WEAPONS[self.weapons[self.num].name]['img_offset'].y

        self.vel.x -= self.knock_back.x
        self.vel.y += self.knock_back.y

        # check hit box collisions
        self.hit_box.x += self.vel.x * dt
        if not server:
            self.collide_with_walls("x")

        self.hit_box.y += self.vel.y * dt
        if not server:
            self.collide_with_walls("y")

        self.knock_back.multiply(0)

        self.pos.x = self.hit_box.x + self.hit_box.width / 2
        self.pos.y = self.hit_box.y + self.hit_box.height / 2

        o = WEAPONS[self.weapons[self.num].name]['offset'].copy().rotate(-self.rot)

        self.o = Vector(self.pos.x, self.pos.y)

        self.o.x += o.x
        self.o.y += o.y

        if self.last_shot > 0:
            self.last_shot -= dt

        if not self.game.buy_menu:
            self.rotate_to_mouse()

        self.sprite.update(rotation=self.rot)

        self.sprite.x = self.hit_box.get_center().x
        self.sprite.y = self.hit_box.get_center().y

        self.weapons[self.num].update(dt)

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

    def draw(self):
        s = self.game.mouse.get_map_pos()

        pyglet.gl.glBegin(pyglet.gl.GL_LINES)
        pyglet.gl.glVertex2i(int(self.pos.x), int(self.pos.y))
        pyglet.gl.glVertex2i(int(s.x), int(s.y))
        pyglet.gl.glEnd()

        pyglet.gl.glBegin(pyglet.gl.GL_LINES)
        pyglet.gl.glVertex2i(int(self.o.x), int(self.o.y))
        pyglet.gl.glVertex2i(int(s.x), int(s.y))
        pyglet.gl.glEnd()


        self.draw_hit_box()
        self.sprite.draw()

class Mouse:
    def __init__(self, sprite, game):
        self.pos = Vector(0, 0)
        self.game = game

        if sprite is not None:
            self.sprite = sprite
            self.width = self.sprite.width
            self.height = self.sprite.height

    def get_map_pos(self):
        return Vector(self.pos.x - self.game.camera.x, self.pos.y - self.game.camera.y)

    def update(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

        if self.pos.x < 0:
            self.pos.x = 0

        elif self.pos.x > WINDOW_WIDTH:
            self.pos.x = WINDOW_WIDTH

        if self.pos.y < 0:
            self.pos.y = 0

        elif self.pos.y > WINDOW_HEIGHT:
            self.pos.y = WINDOW_HEIGHT


        self.sprite.x = self.pos.x - self.sprite.width / 2
        self.sprite.y = self.pos.y - self.sprite.height / 2

    def draw(self):
        self.sprite.draw()

class Wall:
    def __init__(self, x, y, width, height):
        self.pos = Vector(x, y)
        self.width = width
        self.height = height

        self.center = Vector(x + width / 2, y + height / 2)

    def __str__(self):
        return str([self.pos.x, self.pos.y, self.width, self.height])

    def draw(self):
        glBegin(GL_LINES)

        glVertex2i(int(self.pos.x), int(self.pos.y))
        glVertex2i(int(self.pos.x), int(self.pos.y + self.height))

        glVertex2i(int(self.pos.x), int(self.pos.y + self.height))
        glVertex2i(int(self.pos.x + self.width), int(self.pos.y + self.height))

        glVertex2i(int(self.pos.x + self.width), int(self.pos.y + self.height))
        glVertex2i(int(self.pos.x + self.width), int(self.pos.y))

        glVertex2i(int(self.pos.x + self.width), int(self.pos.y))
        glVertex2i(int(self.pos.x), int(self.pos.y))

        glEnd()

class Item:
    def __init__(self, x, y, item):
        self.pos = Vector(x, y)

        self.sprite = Sprite(ITEM_IMAGES[item])

        self.sprite.image.anchor_x = self.sprite.width / 2
        self.sprite.image.anchor_y = self.sprite.height / 2

        self.sprite.x = x
        self.sprite.y = y
