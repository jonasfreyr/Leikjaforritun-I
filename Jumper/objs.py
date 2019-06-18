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