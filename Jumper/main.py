import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite
from settings import *
from objs import *

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_location(500, 500)

        self.frame_rate = 1 / fps

        self.keys = {}

        self.main_batch = pyglet.graphics.Batch()

        background_img = preload_img("maxresdefault.jpg")

        self.backgrounds = []
        x = 0
        for i in range(2):
            self.backgrounds.append(Background(x, 0, Sprite(background_img, batch=self.main_batch)))

            x = self.backgrounds[i].posx + self.backgrounds[i].width

            self.backgrounds[i].velx = background_speed

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

    def update(self, dt):
        for background in self.backgrounds:
            background.update(dt)
            print(background.posx)

            if background.posx + background.width <= 0:
                print("big yay")
                background.posx = background.width
        print("----------")

    def on_draw(self):
        self.clear()

        self.main_batch.draw()

g = Game(width, height, "Big lel", resizable=False)
pyglet.clock.schedule_interval(g.update, g.frame_rate)
pyglet.app.run()