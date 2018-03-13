import pygame as pg
from settings import *
from Cell import *
from os import *
import random

pg.init()


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()

        #self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        self.arrow = pg.image.load(path.join(img_folder, 'arrow.png')).convert_alpha()
        self.arrow = pg.transform.scale(self.arrow, (25, 25))
        self.arrow = pg.transform.rotate(self.arrow, 180)

    def new(self):
        self.load_data()

        self.all_sprites = pg.sprite.Group()
        self.cells = pg.sprite.Group()
        self.food = pg.sprite.Group()
        self.poison = pg.sprite.Group()

        for a in range(30):
            Poison(self, random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20))

        for a in range(10):
            Cell(self, random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(SPEED[0], SPEED[1]), random.randint(50, 200), random.randint(50, 200), random.uniform(0.8, 1.5), random.uniform(0.2, 1.2))

        for a in range(100):
            Food(self, random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20))

        self.loop()

    def update(self):
        self.all_sprites.update()

        pct = random.random()
        if pct < 0.01:
            Food(self, random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20))

        if pct > 0.99:
            Food(self, random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20))

        pg.sprite.groupcollide(self.food, self.cells, True, False)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                quit()

    def loop(self):
        while True:
            pg.display.set_caption(str(self.clock.get_fps()))

            self.dt = self.clock.tick(FPS) / 1000

            self.events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

            pg.display.flip()

    def draw(self):
        self.screen.fill((255, 255, 255))

        for sprite in self.cells:
            self.screen.blit(sprite.image, sprite.rect)
            pg.draw.circle(self.screen, GREEN, (int(sprite.pos.x), int(sprite.pos.y)), sprite.detect_radius_food, 1)
            pg.draw.circle(self.screen, RED, (int(sprite.pos.x), int(sprite.pos.y)), sprite.detect_radius_poison, 1)

        for sprite in self.food:
            self.screen.blit(sprite.image, sprite.rect)

        for sprite in self.poison:
            self.screen.blit(sprite.image, sprite.rect)



h = Game()

h.new()