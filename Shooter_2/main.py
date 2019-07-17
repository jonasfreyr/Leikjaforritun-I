import pyglet
from settings import *
from map import *
from os import path
from objs import *
from pyglet.sprite import Sprite
from pyglet.window import key

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_location(30, 500)

        self.frame_rate = 1 / FPS

        self.keys = {key.A: False, key.W: False, key.D: False, key.S: False}

        self.load()
        self.new()

    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

    def load(self):
        game_folder = path.dirname(__file__)
        res_folder =  path.join(game_folder, "res")
        img_folder = path.join(res_folder, "img")
        self.map_folder = path.join(res_folder, "maps")

        self.player_images = {}
        for a in PLAYER_IMAGES:
            p = preload_img(PLAYER_IMAGES[a])
            texture = p.get_texture()
            texture.width = TILESIZE
            texture.height = TILESIZE

            self.player_images[a] = p

    def new(self):
        self.map = TiledRenderer(path.join(self.map_folder, "map1.tmx"))

        for tile_object in self.map.tmx_data.objects:
            pos = Vector(tile_object.x, (self.map.size[1] - tile_object.y - tile_object.height))
            if tile_object.name == "Player":
                self.player = Player(pos.x, pos.y, Sprite(self.player_images["pistol"]), self)

        self.camera = Camera()

    def update(self, dt):
        # print(self.player.pos.x)

        self.player.vel.multiply(0)

        if self.keys[key.W]:
            self.player.vel.y += PLAYER_SPEED

        if self.keys[key.S]:
            self.player.vel.y += -PLAYER_SPEED

        if self.keys[key.D]:
            self.player.vel.x += PLAYER_SPEED

        if self.keys[key.A]:
            self.player.vel.x += -PLAYER_SPEED
            # print("yay")

        self.player.update(dt)

    def on_draw(self):
        self.clear()

        pyglet.gl.glPushMatrix()
        self.camera.draw(self.player)
        self.map.draw()

        self.player.draw()
        pyglet.gl.glPopMatrix()

g = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "Shooter 2", resizable=False, vsync=False)
pyglet.clock.schedule_interval(g.update, g.frame_rate)
pyglet.app.run()























































