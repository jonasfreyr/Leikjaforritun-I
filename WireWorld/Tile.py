import pygame as pg
from settings import *

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, game, state="none"):
        self.group = game.tiles
        pg.sprite.Sprite.__init__(self, self.group)

        self.x = x
        self.y = y

        self.size = tile_size

        self.rect = pg.Rect(x, y, self.size, self.size)
        self.game = game

        self.state = state
        self.color = states[state]

    def update(self):
        pass
