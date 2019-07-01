import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite
from settings import *
from objs import *
import random

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_location(30, 500)

        self.frame_rate = 1 / fps

        self.keys = {}
        self.keys[key.SPACE] = False

        self.main_batch = pyglet.graphics.Batch()

        self.speed = background_speed

        background_img = preload_img("maxresdefault.jpg")
        player_img = preload_img("dino.png")

        self.player = Player(Sprite(player_img))

        self.backgrounds = []
        x = 0
        for i in range(2):
            self.backgrounds.append(Background(x, 0, Sprite(background_img, batch=self.main_batch)))

            x = self.backgrounds[i].posx + self.backgrounds[i].width

            self.backgrounds[i].velx = self.speed

        self.objs = []

        self.rock_img = preload_img("rock.png")
        texture = self.rock_img.get_texture()
        texture.width = 60
        texture.height = 60


        self.counter = 0
        self.spawn_counter = 0

        self.points = 0
        self.num = 0

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

    def update(self, dt):
        self.player.update(dt)

        if self.keys[key.SPACE]:
            self.player.jump(dt)

        for background in self.backgrounds:
            background.update(dt)

            background.velx = self.speed

        for obj in self.objs:
            if obj.posx < 0 - obj.width:
                self.objs.remove(obj)

            obj.update(dt)

            obj.velx = self.speed

        for i in range(len(self.backgrounds)):
            if self.backgrounds[i].posx + self.backgrounds[i].width <= 0:
                if i == 0:
                    self.backgrounds[i].posx = self.backgrounds[i + 1].posx + self.backgrounds[i + 1].width

                elif i == 1:
                    self.backgrounds[i].posx = self.backgrounds[i - 1].posx + self.backgrounds[i - 1].width


        self.counter += dt
        self.spawn_counter += dt

        self.points = abs(self.speed + abs(background_speed))

        print(self.objs)

        if self.spawn_counter > self.num:
            self.num = random.randint(1, 3)
            self.objs.append(Obstacle(width, bottom, Sprite(self.rock_img, batch=self.main_batch)))
            self.spawn_counter = 0

        if self.counter >= 1:
            self.speed -= 5
            self.counter = 0

    def on_draw(self):
        self.clear()

        self.main_batch.draw()

        self.player.draw()

g = Game(width, height, "Big lel", resizable=False)
pyglet.clock.schedule_interval(g.update, g.frame_rate)
pyglet.app.run()