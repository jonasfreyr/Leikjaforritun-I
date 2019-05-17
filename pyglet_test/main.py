import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.sprite import Sprite
from GameObjects import *

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(1000, 50)
        self.fps_draw = FPSDisplay(self)
        self.fps_draw.label.font_size = 50
        self.fps_draw.label.y = 800 - 50 - 10

        self.frame_rate = 1/60.0

    def load_data(self):
        player_sprite = Sprite(preload_img("PlayerShip.png"))
        space_sprite = preload_img("space.jpg")

        self.player = GameObject(500, 100, player_sprite)

        self.space_list = []
        for i in range(2):
            self.space_list.append(GameObject(0, i * 1200, Sprite(space_sprite)))

            self.space_list[i].vely = -600

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.player.velx = 300

        if symbol == key.LEFT:
            self.player.velx = -300

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.RIGHT, key.LEFT):
            self.player.velx = 0

    def on_draw(self):
        self.clear()

        for space in self.space_list:
            space.draw()

        self.player.draw()

        self.fps_draw.draw()

    def update_space(self, dt):
        for space in self.space_list:
            space.update(dt)
            if space.posy <= -1300:
                space.posy = 1000

    def update(self, dt):
        self.update_space(dt)

        self.player.update(dt)

g = GameWindow(800, 800, "Space Invaders", resizable=False)
g.load_data()
pyglet.clock.schedule_interval(g.update, g.frame_rate)
pyglet.app.run()