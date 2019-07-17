import pyglet
from vector import Vector
from settings import *

class Player:
    def __init__(self, x, y, sprite, game):
        self.pos = Vector(x, y)
        self.vel = Vector(x, y)

        self.game = game

        if sprite is not None:
            self.sprite = sprite
            self.width = self.sprite.width
            self.height = self.sprite.height
        

    def update(self, dt):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        self.sprite.x = self.pos.x
        self.sprite.y = self.pos.y

    def draw(self):
        self.sprite.draw()
