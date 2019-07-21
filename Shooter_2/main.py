import pyglet
from map import *
from os import path
from objs import *
from pyglet.sprite import Sprite
from pyglet.window import key
from hud import *

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs).__init__(vsync=False)

        self.frame_rate = 1 / FPS

        pyglet.clock.schedule_interval(self.update, self.frame_rate)
        pyglet.clock.set_fps_limit(FPS)

        self.set_location(30, 500)

        self.keys = {key.A: False, key.W: False, key.D: False, key.S: False}

        self.load()
        self.new()

        self.set_exclusive_mouse(True)

        self.mouse_down = False

    def on_key_press(self, symbol, modifiers):
        """
        When a key is pressed on
        the keyboard.

        :param symbol:
        :param modifiers:
        :return: None
        """
        self.keys[symbol] = True

        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

        if symbol == key.R:
            self.player.weapon.reload()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse.update(dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.mouse_down = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.mouse_down = False

            self.player.weapon.reset()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.update(dx, dy)

    def load(self):
        game_folder = path.dirname(__file__)
        res_folder =  path.join(game_folder, "res")
        img_folder = path.join(res_folder, "img")
        self.map_folder = path.join(res_folder, "maps")

        self.player_images = {}
        for a in PLAYER_IMAGES:
            p = preload_img(PLAYER_IMAGES[a])
            texture = p.get_texture()
            texture.width = WEAPONS[a]["img_size"].x
            texture.height = WEAPONS[a]["img_size"].y

            self.player_images[a] = p

        self.crosshair_img = preload_img(CROSSHAIR_IMG)

        texture = self.crosshair_img.get_texture()
        texture.width = CROSSHAIR_WIDTH
        texture.height = CROSSHAIR_HEIGHT

        self.bullet_img = preload_img("bullet.png")

        # x = texture.width / 2
        # y = texture.height / 2

        # cursor = pyglet.window.ImageMouseCursor(crosshair_img, x, y)
        # self.set_mouse_cursor(cursor)

        self.muzzle_flash_img = preload_img("muzzleFlash.png")
        texture = self.muzzle_flash_img.get_texture()
        texture.width = MUZZLE_FLASH_SIZE.x
        texture.height = MUZZLE_FLASH_SIZE.y

    def new(self):
        self.main_batch = pyglet.graphics.Batch()
        self.bullet_batch = pyglet.graphics.Batch()
        self.effects_batch = pyglet.graphics.Batch()
        self.hud_batch = pyglet.graphics.Batch()

        self.map = TiledRenderer(path.join(self.map_folder, "map1.tmx"))

        self.hud_labels = []
        self.walls = []
        self.effects = []

        for tile_object in self.map.tmx_data.objects:
            pos = Vector(tile_object.x, (self.map.size[1] - tile_object.y - tile_object.height))
            pos.x = pos.x + tile_object.width / 2
            pos.y = pos.y + tile_object.height / 2
            if tile_object.name == "Wall":
                self.walls.append(Wall(tile_object.x, pos.y - tile_object.height / 2, tile_object.width, tile_object.height))

            elif tile_object.name == "Player":
                self.player = Player(pos.x, pos.y, Sprite(self.player_images[tile_object.type]), self, tile_object.type)

        self.bullets = []

        self.camera = Camera()

        self.mouse = Mouse(Sprite(self.crosshair_img), self)

        # Hud Labels
        #   Ammo Label
        l =  pyglet.text.Label("big lel", x=WINDOW_WIDTH, y=0, batch=self.hud_batch)
        l.anchor_x = "right"
        l.font_size = FONT_SIZE
        self.hud_labels.append(AmmoText(self, l))

        self.target = self.player

    def update(self, dt):
        # print(len(self.bullets))
        # print(len(self.effects))

        for label in self.hud_labels:
            label.update()

        if self.mouse_down:
            self.player.shoot()

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

        for bullet in self.bullets:
            bullet.update(dt)

            if bullet.distance > WEAPONS[bullet.weapon]["bullet_distance"] or bullet.check(self):
                bullet.sprite.delete()
                self.bullets.remove(bullet)

        for effect in self.effects:
            effect.update(dt)

            if effect.dead:
                self.effects.remove(effect)

        self.player.update(dt)

    def on_draw(self):
        pyglet.clock.tick()

        self.clear()

        pyglet.gl.glPushMatrix()
        self.camera.draw(self.target)
        self.map.draw()
        self.main_batch.draw()
        self.player.draw()
        self.bullet_batch.draw()
        self.effects_batch.draw()

        for wall in self.walls:
            wall.draw()

        pyglet.gl.glPopMatrix()

        self.hud_batch.draw()

        self.mouse.draw()

g = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "Shooter 2", resizable=False)


pyglet.app.run()























































