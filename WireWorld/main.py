import pygame as pg
from settings import *

pg.init()

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((ww, wh))
        self.clock = pg.time.Clock()

    def new(self):
        pass

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                quit()

    def draw(self):
        self.screen.fill((0, 0, 0))

    def update(self):
        pass

    def loop(self):
        while True:
            self.event()
            self.draw()
            self.update()

G = Game()

G.new()
G.loop()