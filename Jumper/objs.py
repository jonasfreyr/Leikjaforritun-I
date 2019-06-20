import pyglet
from settings import *


def preload_img(img):
    return pyglet.image.load("res/images/" + img)

class Background:
    def __init__(self, posx, posy, sprite=None):
        self.posx = posx
        self.posy = posy

        self.velx = 0
        self.vely = 0

        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.posx
            self.sprite.y = self.posy
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.posx += self.velx * dt

        self.sprite.x = self.posx
        self.sprite.y = self.posy

class Player:
    def __init__(self, sprite):
        self.posy = bottom

        self.originaly = bottom
        self.vely = 0

        self.jumped = False

        if sprite is not None:
            self.sprite = sprite
            self.sprite.update(scale=0.15)
            self.sprite.y = self.posy
            self.width = self.sprite.width
            self.height = self.sprite.height

    def jump(self, dt):
        if not self.jumped:
            self.vely = jump_speed * dt
            self.jumped = True

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.vely -= gravity * dt

        self.posy += self.vely

        if self.posy < self.originaly:
            self.posy = self.originaly
            self.jumped = False

        self.sprite.y = self.posy

class Obstacle:
    def __init__(self, x, y, sprite):
        self.posx = x
        self.posy = y

        self.velx = 0
        self.vely = 0

        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.posx
            self.sprite.y = self.posy
            self.width = self.sprite.width
            self.height = self.sprite.height

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.posx += self.velx * dt

        self.sprite.x = self.posx
        self.sprite.y = self.posy
