import pyglet
from vector import Vector
from settings import *
from pyglet.gl import *
from pyglet.sprite import Sprite
# import pygame as pg
import math
from weapons import Weapon

class Player:
    def __init__(self, x, y, sprite, game, weapon):
        self.pos = Vector(x, y)
        self.vel = Vector(x, y)

        self.rot = 0

        self.game = game

        self.weapon = Weapon(weapon)

        self.last_shot = 0

        self.hit_box = PLAYER_HIT_BOX
        self.hit_box.x = x
        self.hit_box.y = y

        if sprite is not None:
            self.sprite = sprite
            self.width = self.sprite.width
            self.height = self.sprite.height

        self.sprite.image.anchor_x = self.sprite.image.width / 2 - WEAPONS[weapon]['img_offset'].x
        self.sprite.image.anchor_y = self.sprite.image.height / 2 - WEAPONS[weapon]['img_offset'].y

    def get_rotation(self, point1, point2):
        return math.degrees(math.atan2(point1.x - point2.x, point1.y - point2.y))

    def shoot(self):
        if self.last_shot <= 0:
            o = WEAPONS[self.weapon.name]['offset'].rotate(-self.rot)

            pos = Vector(self.pos.x, self.pos.y)

            pos.x += o.x
            pos.y += o.y

            rot = self.get_rotation(pos, self.game.mouse.get_map_pos()) + 90

            self.weapon.shoot(pos, rot, self.game)

            self.last_shot = WEAPONS[self.weapon.name]["rate"]

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

    def update(self, dt):
        if self.last_shot > 0:
            self.last_shot -= dt

        self.rotate_to_mouse()

        self.sprite.update(rotation=self.rot)

        self.pos.x = self.hit_box.x + self.hit_box.width / 2
        self.pos.y = self.hit_box.y + self.hit_box.height / 2

        # check hit box collisions
        self.hit_box.x += self.vel.x * dt
        self.collide_with_walls("x")

        self.hit_box.y += self.vel.y * dt
        self.collide_with_walls("y")

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

    def draw(self):
        s = self.game.mouse.get_map_pos()

        pyglet.gl.glBegin(pyglet.gl.GL_LINES)
        pyglet.gl.glVertex2i(int(self.pos.x), int(self.pos.y))
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
