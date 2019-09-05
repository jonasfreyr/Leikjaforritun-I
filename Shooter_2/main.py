import pyglet
from map import *
from os import path
from objs import *
from pyglet.sprite import Sprite
from pyglet.window import key
from hud import *
from weapons import *
import _thread, socket, site, os, sys

print(site.getsitepackages())
print(os.path.dirname(sys.executable))

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs).__init__(vsync=False)

        self.frame_rate = 1 / FPS

        pyglet.clock.schedule_interval(self.update, self.frame_rate)
        pyglet.clock.set_fps_limit(FPS)

        self.set_location(1000, 500)

        self.keys = {key.A: False, key.W: False, key.D: False, key.S: False}

        # self.set_exclusive_mouse(True)

        self.mouse_down = False

        self.respawn = False

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
            self.respawn = True

        elif symbol == key.Q:
            self.player.switch()

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

        # Grenades Logos
        self.grenade_logo = preload_img(GRENADE_LOGO)
        texture = self.grenade_logo.get_texture()
        texture.width = GRENADE_LOGO_SIZE.x
        texture.height = GRENADE_LOGO_SIZE.y

        self.smoke_logo = preload_img(SMOKE_LOGO)
        texture = self.smoke_logo.get_texture()
        texture.width = SMOKE_LOGO_SIZE.x
        texture.height = SMOKE_LOGO_SIZE.y


        self.ak47_logo = preload_img(AK47_LOGO)
        texture = self.ak47_logo.get_texture()
        texture.width = AK47_LOGO_SIZE.x
        texture.height = AK47_LOGO_SIZE.y

        self.pistol_logo = preload_img(PISTOL_LOGO)
        texture = self.pistol_logo.get_texture()
        texture.width = PISTOL_LOGO_SIZE.x
        texture.height = PISTOL_LOGO_SIZE.y

        self.shotgun_logo = preload_img(SHOTGUN_LOGO)
        texture = self.shotgun_logo.get_texture()
        texture.width = SHOTGUN_LOGO_SIZE.x
        texture.height = SHOTGUN_LOGO_SIZE.y

        _thread.start_new_thread(self.receive_data, (s, 2))
        self.s = s

    def new(self):
        self.main_batch = pyglet.graphics.Batch()
        self.bullet_batch = pyglet.graphics.Batch()
        self.effects_batch = pyglet.graphics.Batch()
        self.hud_batch = pyglet.graphics.Batch()
        self.hud_logo_batch = pyglet.graphics.Batch()
        self.o_players_batch = pyglet.graphics.Batch()

        self.map = TiledRenderer(path.join(self.map_folder, MAP))

        self.hud_labels = []
        self.walls = []
        self.effects = []
        self.grenades = []
        self.o_players = []
        self.weapon_logos = {}
        self.o_bullets = []
        self.new_bullets = []
        self.new_grenades = []
        self.o_grenades = []

        # self.s_bullets = []
        # self.s_grenades = []

        for tile_object in self.map.tmx_data.objects:
            pos = Vector(tile_object.x, (self.map.size[1] - tile_object.y - tile_object.height))
            pos.x = pos.x + tile_object.width / 2
            pos.y = pos.y + tile_object.height / 2
            if tile_object.name == "Wall":
                self.walls.append(Wall(tile_object.x, pos.y - tile_object.height / 2, tile_object.width, tile_object.height))

            elif tile_object.name == "Player":
                self.player = Player(pos.x, pos.y, self, tile_object.type)
                self.r_pos = pos.copy()
                if tile_object.type == 'None':
                    self.r_wep = "pistol"
                else:
                    self.r_wep = tile_object.type

        self.bullets = []

        self.camera = Camera()

        self.mouse = Mouse(Sprite(self.crosshair_img), self)

        # self.hud_labels.append(Logo(SMOKE_LOGO_POS ,Sprite(self.smoke_logo, batch=self.hud_batch), self))

        #   Ammo Label
        l =  pyglet.text.Label("big lel", x=WINDOW_WIDTH, y=0, batch=self.hud_batch)
        l.anchor_x = "right"
        l.font_size = FONT_SIZE
        self.hud_labels.append(AmmoText(self, l))

        l = pyglet.text.Label("big lel 2", x=0, y=0, batch=self.hud_batch)
        l.font_size = FONT_SIZE
        self.hud_labels.append(Health(self, l))

        self.target = self.player

    def receive_data(self, conn, i):
        while True:
            data = conn.recv(262144).decode()

            data = eval(data)

            i_ids = []
            # print(data)
            for ids in data["players"]:
                i_ids.append(ids)
                for player in self.o_players:
                    if ids == player.id:
                        player.rot = data["players"][ids]["rot"]
                        player.pos.x = data["players"][ids]["pos"]["x"]
                        player.pos.y = data["players"][ids]["pos"]["y"]
                        player.weapon = data["players"][ids]["weapon"]
                        player.dead = data["players"][ids]["dead"]
                        break

                else:
                    self.o_players.append(Oplayers(ids, Vector(data["players"][ids]["pos"]["x"], data["players"][ids]["pos"]["x"]), data["players"][ids]["rot"], data["players"][ids]["weapon"], self))

            for player in self.o_players:
                if player.id not in i_ids:
                    self.o_players.remove(player)

            self.new_bullets = data["bullets"]
            self.new_grenades = data["grenades"]

            self.player.health = data["health"]

    def reset(self):
        self.player.hit_box.x = self.r_pos.x
        self.player.hit_box.y = self.r_pos.y


        self.player.weapon = Weapon(self.r_wep)

        if self.r_wep != "pistol":
            self.player.other_weapon = Weapon("pistol")

        self.player.grenades = [Grenade(self, "smoke"),Grenade(self, "grenade"),Grenade(self, "smoke"),Grenade(self, "grenade"),Grenade(self, "smoke")]

    def update(self, dt):
        # print(self.o_bullets)
        # print(len(self.bullets))
        # print(len(self.effects))
        # print(len(self.grenades))
        # print(len(self.o_players))
        # print(self.new_grenades)
        # print(self.player.pos)
        # print(self.player.other_weapon)

        if self.player.health <= 0:
            try:
                self.target = self.o_players[0]

            except:
                self.target = self.player

        else:
            self.target = self.player

        self.bullets = []
        for bullet in self.new_bullets:
            self.bullets.append(O_Bullet(bullet["pos"]["x"], bullet["pos"]["y"], bullet["rot"], bullet["weapon"], self))


        self.grenades = []
        for grenade in self.new_grenades:
            g = O_Grenade(grenade["pos"]["x"], grenade["pos"]["y"], grenade["type"], self)

            if grenade["exploded"]:
                g.explode()
                if grenade["type"] == "smoke":
                    g.sprite.opacity = grenade["opacity"]

            self.grenades.append(g)

        # print(self.bullets)

        self.hud_logos = []
        smoke_pos = SMOKE_LOGO_POS + SMOKE_LOGO_PADDING
        grenade_pos = GRENADE_LOGO_POS + GRENADE_LOGO_PADDING

        for grenade in self.player.grenades:
            if grenade.type == "grenade":
                self.hud_logos.append(Logo(grenade_pos, Sprite(self.grenade_logo, batch=self.hud_batch), self))

                grenade_pos.x = grenade_pos.x - GRENADE_LOGO_SIZE.x

            elif grenade.type == "smoke":
                self.hud_logos.append(Logo(smoke_pos, Sprite(self.smoke_logo, batch=self.hud_batch), self))

                smoke_pos.x = smoke_pos.x - SMOKE_LOGO_SIZE.x

        if self.player.weapon.name == "rifle":
            self.hud_logos.append(Logo(AK47_LOGO_POS, Sprite(self.ak47_logo, batch=self.hud_batch), self))

        elif self.player.weapon.name == "pistol":
            self.hud_logos.append(Logo(PISTOL_LOGO_POS, Sprite(self.pistol_logo, batch=self.hud_batch), self))

        elif self.player.weapon.name == "shotgun":
            self.hud_logos.append(Logo(SHOTGUN_LOGO_POS, Sprite(self.shotgun_logo, batch=self.hud_batch), self))

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

        for effect in self.effects:
            effect.update(dt)

            if effect.dead:
                self.effects.remove(effect)

        self.player.update(dt)

        for player in self.o_players:
            player.update()

        if self.respawn:
            self.reset()

        data = {"player": {"pos": {"x": self.player.pos.x, "y": self.player.pos.y}, "rot": self.player.rot,
                           "weapon": self.player.weapon.name, "respawn": self.respawn}, "bullets": [],
                "grenades": []}

        tempB = list(self.o_bullets)
        for bullet in tempB:
            data["bullets"].append(bullet)
            self.o_bullets.remove(bullet)

        tempG = list(self.o_grenades)
        for grenade in tempG:
            data["grenades"].append(grenade)
            self.o_grenades.remove(grenade)

        self.s.sendall(str(data).encode())

        if self.respawn:
            self.respawn = False

    def on_draw(self):
        pyglet.clock.tick()

        self.clear()

        pyglet.gl.glPushMatrix()
        self.camera.draw(self.target)
        self.map.draw()
        self.main_batch.draw()
        if self.player.health > 0:
            self.player.draw()

        for player in self.o_players:
            if not player.dead:
                player.sprite.draw()

        self.bullet_batch.draw()

        self.effects_batch.draw()

        for wall in self.walls:
            wall.draw()

        pyglet.gl.glPopMatrix()

        self.hud_batch.draw()

        self.mouse.draw()

g = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "Shooter 2", resizable=False)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    g.load()
    g.new()

    pyglet.app.run()