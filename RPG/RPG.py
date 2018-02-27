import pygame as pg
from settings import *
from sprites import *
from os import path
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("RPG")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.gp = False
        pg.key.set_repeat(500, 100)

    def quit(self):
        quit()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map2.txt'))

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()


        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)

                elif tile.lower() == 'p':
                    self.player = Player(self, col, row)
            self.camera = Camera(self.map.width, self.map.height)

        self.loop()

    def loop(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.gp == False:
                self.update()
            self.draw()

            self.clock.tick(FPS)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                self.quit()

            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    self.gp = not self.gp

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGROUND)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def go_screen(self):
        pass

    def start_screen(self):
        pass

H = Game()
while True:
    H.new()
H.go_screen()