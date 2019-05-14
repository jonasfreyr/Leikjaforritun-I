import pygame as pg
from settings import *
from Tile import *
from camera import *
import random

pg.init()

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((camera_width, camera_height))
        self.clock = pg.time.Clock()

        self.keys = {}

        self.keys[pg.K_UP] = False
        self.keys[pg.K_DOWN] = False
        self.keys[pg.K_LEFT] = False
        self.keys[pg.K_RIGHT] = False

    def new(self):
        self.tiles = pg.sprite.Group()

        self.player = Player(camera_width / 2, camera_height / 2)
        self.camera = Camera(ww, wh)
        self.mouse = Mouse()

        y = 0
        for a in range(grid_height):
            x = 0
            for b in range(grid_width):
                # Tile(x, y, self, "none")
                Tile(x, y, self, random.choice(list(states.keys())))
                x += tile_size

            y += tile_size

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                quit()

            if event.type == pg.KEYDOWN:
                self.keys[event.key] = True

            elif event.type == pg.KEYUP:
                self.keys[event.key] = False

        if self.keys[pg.K_UP]:
            self.player.y -= camera_speed

        if self.keys[pg.K_DOWN]:
            self.player.y += camera_speed

        if self.keys[pg.K_RIGHT]:
            self.player.x += camera_speed

        if self.keys[pg.K_LEFT]:
            self.player.x -= camera_speed

    def draw(self):
        self.screen.fill((0, 0, 0))
        for tile in self.tiles:
            if collide_rect(self.player, tile):
                if tile.state != "none" and tile.state != "hover":
                    pg.draw.rect(self.screen, tile.color, self.camera.apply_rect(tile.rect))

                elif tile.state == "hover":
                    s = pg.Surface((tile.size, tile.size), pg.SRCALPHA)
                    s.fill(hover)
                    self.screen.blit(s, (tile.x, tile.y))

        pg.display.flip()

    def update(self):
        self.player.update()
        self.camera.update(self.player)
        self.mouse.update()

        for tile in self.tiles:
            tile.update()

    def loop(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            pg.display.set_caption(str(self.clock.get_fps()))


G = Game()
G.new()
G.loop()
