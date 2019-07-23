import pyglet
from map import *
from os import path
from objs import *
from pyglet.sprite import Sprite
from pyglet.window import key
from hud import *
from weapons import Grenade

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

        elif symbol == key.R:
            self.player.weapon.reload()

        elif symbol == key.G:
            self.player.throw(self.dt)

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

        if symbol == key.SPACE:
            self.new()

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

        self.bullet_img = preload_img(BULLET_IMG)

        # x = texture.width / 2
        # y = texture.height / 2

        # cursor = pyglet.window.ImageMouseCursor(crosshair_img, x, y)
        # self.set_mouse_cursor(cursor)

        self.muzzle_flash_img = preload_img(MUZZLE_FLASH_IMG)
        texture = self.muzzle_flash_img.get_texture()
        texture.width = MUZZLE_FLASH_SIZE.x
        texture.height = MUZZLE_FLASH_SIZE.y

        self.granade_img = preload_img(GRENADE_IMG)
        texture = self.granade_img.get_texture()
        texture.width = GRENADE_SIZE.x
        texture.height = GRENADE_SIZE.y

        explosion = preload_img(EXPLOSION_IMG)
        explosion_seq = pyglet.image.ImageGrid(explosion, 4, 5, item_width=96, item_height=96)
        self.explosion_anim = pyglet.image.Animation.from_image_sequence(explosion_seq[0:], EXPLOSION_DURATION, loop=False)

        self.smoke_img = preload_img(SMOKE_GRENADE_IMG)
        texture = self.smoke_img.get_texture()
        texture.width = SMOKE_GRENADE_SIZE.x
        texture.height = SMOKE_GRENADE_SIZE.y

        self.smoke = preload_img(SMOKE_IMG)
        texture = self.smoke.get_texture()
        texture.width = SMOKE_SIZE.x
        texture.height = SMOKE_SIZE.y

        # smoke_seq = pyglet.image.ImageGrid(smoke, 6, 12, item_width=341, item_height=280)
        # self.smoke_anim = pyglet.image.Animation.from_image_sequence(smoke_seq[0:], SMOKE_DURATION, loop=False)

    def new(self):
        self.main_batch = pyglet.graphics.Batch()
        self.bullet_batch = pyglet.graphics.Batch()
        self.effects_batch = pyglet.graphics.Batch()
        self.hud_batch = pyglet.graphics.Batch()

        self.map = TiledRenderer(path.join(self.map_folder, MAP))

        self.hud_labels = []
        self.walls = []
        self.effects = []
        self.grenades = []

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

        # Grenades Logos
        self.grenade_logo = preload_img(GRENADE_LOGO)

        self.target = self.player

    def update(self, dt):
        # print(len(self.bullets))
        # print(len(self.effects))
        # print(len(self.grenades))

        self.dt = dt

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

        for grenade in self.grenades:
            grenade.update(dt)

            if grenade.explode_sprite is not None:
                if grenade.explode_sprite.deleted:
                    self.grenades.remove(grenade)

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

        for grenade in self.grenades:
            grenade.draw_hit_box()

        pyglet.gl.glPopMatrix()

        self.hud_batch.draw()

        self.mouse.draw()

g = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "Shooter 2", resizable=False)


pyglet.app.run()























































