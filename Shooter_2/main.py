import pyglet
from map import *
from os import path
from objs import *
from pyglet.sprite import Sprite
from pyglet.window import key
from hud import *
from weapons import *
import _thread, socket, site, os, sys, platform, random
from pyglet.gl import *


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs).__init__(vsync=False)

        self.frame_rate = 1 / FPS

        pyglet.clock.schedule_interval(self.update, self.frame_rate)
        # pyglet.clock.set_fps_limit(FPS)

        self.set_location(20, 20)

        self.keys = {key.A: False, key.W: False, key.D: False, key.S: False, key.TAB: False}

        # self.set_exclusive_mouse(True)

        self.mouse_down = False
        self.respawn = False

        self.picked = False
        self.buy_menu = False

        self.dc = False

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
            self.player.weapons[self.player.num].reload()

        elif symbol == key.G:
            self.player.throw(self.dt)

        elif symbol == key.TAB:
            tcp_s.sendall(b"get stats")

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

        if self.picked:
            if self.buy_menu is False:
                if symbol == key.SPACE:
                    tcp_s.sendall(b"respawn")

                elif symbol == key.Q:
                    self.player.switch()

            if symbol == key.B:
                if self.can_buy:
                    self.buy_menu = not self.buy_menu

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse.update(dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1 and not self.buy_menu:
            self.mouse_down = True

    def on_mouse_release(self, x, y, button, modifiers):
        global SIDE
        if button == 1:
            self.mouse_down = False

            if self.picked:
                if not self.buy_menu:
                    self.player.weapons[self.player.num].reset()

                else:
                    for box in self.buy_menu_items:
                        if self.mouse.pos.x > box.x - box.content_width / 2 and self.mouse.pos.x < box.x + box.content_width / 2 and self.mouse.pos.y > box.y - box.content_height / 2 and self.mouse.pos.y < box.y + box.content_height / 2:
                            if WEAPONS[box.text]["primary"]:
                                self.player.weapons[0] = Weapon(box.text)

                                if self.player.num == 1:
                                    self.player.num = 0

                            else:
                                self.player.weapons[1] = Weapon(box.text)

                            break

            else:
                if self.mouse.pos.x < WINDOW_WIDTH / 2:
                    SIDE = "T"

                else:
                    SIDE = "CT"

                tcp_s.sendall(SIDE.encode())
                self.new()
                self.picked = True

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.update(dx, dy)

    def load(self):
        osystem = platform.system()

        if osystem == "Linux" or osystem == "Darwin":
            game_folder = os.getcwd()
            res_folder = game_folder + "/res"
            img_folder = res_folder + "/img"
            self.map_folder = res_folder + "/maps"
        elif osystem == "Windows":
            game_folder = path.dirname(__file__)
            res_folder =  path.join(game_folder, "res")
            img_folder = path.join(res_folder, "img")
            self.map_folder = path.join(res_folder, "maps")

        self.player_images = {}

        self.crosshair_img = preload_img(CROSSHAIR_IMG)

        texture = self.crosshair_img.get_texture()
        texture.width = CROSSHAIR_WIDTH
        texture.height = CROSSHAIR_HEIGHT

        self.bullet_img = preload_img(BULLET_IMG)

        self.muzzle_flash_img = preload_img(MUZZLE_FLASH_IMG)
        texture = self.muzzle_flash_img.get_texture()
        texture.width = MUZZLE_FLASH_SIZE.x
        texture.height = MUZZLE_FLASH_SIZE.y

        self.granade_img = preload_img(GRENADE_IMG)
        texture = self.granade_img.get_texture()
        texture.width = GRENADE_SIZE.x
        texture.height = GRENADE_SIZE.y

        explosion = preload_img(EXPLOSION_IMG)
        explosion_seq = pyglet.image.ImageGrid(explosion, 4, 5, item_width=EXPLOSION_ITEM_SIZE.x, item_height=EXPLOSION_ITEM_SIZE.y)
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

        self.weapon_logos = {}

        for weapon in WEAPONS:
            logo = preload_img(WEAPONS[weapon]["logo_img"])
            texture = logo.get_texture()
            size = WEAPONS[weapon]["logo_size"]
            texture.width = size.x
            texture.height = size.y
            self.weapon_logos[weapon] = logo

            p = preload_img(WEAPONS[weapon]["player_image"])
            texture = p.get_texture()
            texture.width = WEAPONS[weapon]["img_size"].x
            texture.height = WEAPONS[weapon]["img_size"].y

            self.player_images[weapon] = p

        pick_img = preload_img(PICK_IMG)
        texture = pick_img.get_texture()
        texture.width = WINDOW_WIDTH
        texture.height = WINDOW_HEIGHT
        self.pick_sprite = Sprite(pick_img)

        self.mouse = Mouse(Sprite(self.crosshair_img), self)

        self.new_players = []

    def new(self):
        _thread.start_new_thread(self.receive_data, (s, 2))
        _thread.start_new_thread(self.recive_dataTCP, (tcp_s, 2))

        self.s = s

        self.main_batch = pyglet.graphics.Batch()
        self.bullet_batch = pyglet.graphics.Batch()
        self.effects_batch = pyglet.graphics.Batch()
        self.hud_batch = pyglet.graphics.Batch()
        self.hud_logo_batch = pyglet.graphics.Batch()
        self.o_players_batch = pyglet.graphics.Batch()
        self.buy_menu_batch = pyglet.graphics.Batch()
        self.stats_batch = pyglet.graphics.Batch()

        self.map = TiledRenderer((self.map_folder + "/" + MAP))

        self.hud_labels = []
        self.walls = []
        self.effects = []
        self.grenades = []
        self.o_players = []
        self.o_bullets = []
        self.new_bullets = []
        self.new_grenades = []
        self.o_grenades = []
        self.stats_list = []

        # self.s_bullets = []
        # self.s_grenades = []

        for tile_object in self.map.tmx_data.objects:
            pos = Vector(tile_object.x, (self.map.size[1] - tile_object.y - tile_object.height))
            pos.x = pos.x + tile_object.width / 2
            pos.y = pos.y + tile_object.height / 2
            if tile_object.name == "Wall":
                self.walls.append(Wall(tile_object.x, pos.y - tile_object.height / 2, tile_object.width, tile_object.height))

            elif tile_object.name == "Spawn":
                self.r_wep = "pistol"
                if tile_object.type == SIDE.lower():
                    self.buy_menu_area = Rect(pos.x - tile_object.width / 2, pos.y - tile_object.height / 2, tile_object.width, tile_object.height)
                    self.player = Player(pos.x, pos.y, self, 'None')

        self.bullets = []

        self.camera = Camera()

        # self.hud_labels.append(Logo(SMOKE_LOGO_POS ,Sprite(self.smoke_logo, batch=self.hud_batch), self))

        #   Ammo Label
        l = pyglet.text.Label("big lel", x=WINDOW_WIDTH, y=0, batch=self.hud_batch)
        l.anchor_x = "right"
        l.font_size = FONT_SIZE
        self.hud_labels.append(AmmoText(self, l))

        l = pyglet.text.Label("big lel 2", x=0, y=0, batch=self.hud_batch)
        l.font_size = FONT_SIZE
        self.hud_labels.append(Health(self, l))

        self.buy_menu_items = []
        y_pos = WINDOW_HEIGHT / 2
        for weapon in WEAPONS:
            l = pyglet.text.Label(weapon, x=WINDOW_WIDTH / 2, y=y_pos, batch=self.buy_menu_batch)
            l.anchor_x = "center"
            l.anchor_y = "center"
            l.font_size = BUY_MENU_FONT_SIZE
            self.buy_menu_items.append(l)

            y_pos += BUY_MENU_FONT_SIZE + BUY_MENU_PADDING

        self.stats = ""

        self.target = self.player

        self.picked = True

    def recive_dataTCP(self, conn, i):
        print("Starting TCP Receive function")
        while True:
            data = conn.recv(204888).decode()

            # print(data)

            if data == "dc":
                self.dc = True
                break

            data = eval(data)

            if data[0] == "stats":
                self.stats = data[1]

            elif data[0] == "reset":
                self.reset(data[1])

    def receive_data(self, conn, i):
        print("Starting UDP Receive function")
        while True:
            data, address = conn.recvfrom(262144)

            data = eval(data.decode())

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
                    # print(ids)
                    self.new_players.append([ids, data["players"][ids]["pos"]["x"], data["players"][ids]["pos"]["y"], data["players"][ids]["rot"], data["players"][ids]["weapon"]])

            for player in self.o_players:
                if player.id not in i_ids:
                    player.sprite.delete()
                    self.o_players.remove(player)

            self.new_bullets = data["bullets"]
            self.new_grenades = data["grenades"]

            self.player.health = data["health"]

    def reset(self, pos):
        self.player.hit_box.x = pos[0]
        self.player.hit_box.y = pos[1]

        self.player.weapons = [None, Weapon(self.r_wep)]
        self.player.num = 1

        self.player.grenades = [Grenade(self, "smoke"),Grenade(self, "grenade"),Grenade(self, "smoke"),Grenade(self, "grenade"),Grenade(self, "smoke")]

    def update(self, dt):
        # print(self.o_bullets)
        # print(len(self.bullets))
        # print(len(self.effects))
        # print(len(self.grenades))

        # print(self.new_grenades)
        # print(self.player.pos)
        # print(self.player.other_weapon)
        # print(self.stats)
        if self.picked:
            # print(len(self.o_players))
            self.can_buy = False
            if self.player.health <= 0:

                for player in self.o_players:
                    if not player.dead:
                        self.target = player
                        break
                else:
                    self.target = self.player

            else:
                self.target = self.player

                if self.player.pos.x > self.buy_menu_area.x and self.player.pos.x < self.buy_menu_area.x + self.buy_menu_area.width \
                        and self.player.pos.y > self.buy_menu_area.y and self.player.pos.y < self.buy_menu_area.y + self.buy_menu_area.height:
                    self.can_buy = True

                else:
                    self.buy_menu = False

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

            self.hud_logos.append(Logo(WEAPONS[self.player.weapons[self.player.num].name]["logo_pos"], Sprite(self.weapon_logos[self.player.weapons[self.player.num].name], batch=self.hud_batch), self))

            update_stats(self.stats, self, ID)

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

            data = {"id": ID, "player": {"pos": {"x": self.player.pos.x, "y": self.player.pos.y}, "rot": self.player.rot,
                               "weapon": self.player.weapons[self.player.num].name}, "bullets": [],
                    "grenades": []}

            tempB = list(self.o_bullets)
            for bullet in tempB:
                data["bullets"].append(bullet)
                self.o_bullets.remove(bullet)

            tempG = list(self.o_grenades)
            for grenade in tempG:
                data["grenades"].append(grenade)
                self.o_grenades.remove(grenade)

            self.s.sendto(str(data).encode(), addr)

        if len(self.new_players) != 0:
            print(self.new_players)
            for player in self.new_players:
                print(self.o_players)
                pl = [p for p in self.o_players if player[0] == p.id]
                print(pl)
                if len(pl) == 0:
                    print(player[0])
                    self.o_players.append(Oplayers(player[0], Vector(player[1], player[2]), player[3], player[4], self))

            self.new_players = []

        if self.dc:
            sys.exit()

    def on_draw(self):
        pyglet.clock.tick()

        self.clear()

        if self.picked:
            pyglet.gl.glPushMatrix()
            self.camera.draw(self.target)
            self.map.draw()
            self.main_batch.draw()
            if self.player.health > 0:
                self.player.draw()

            for player in self.o_players:
                if not player.dead:
                    if self.player.see_player(player) or self.player.health <= 0:
                        player.sprite.draw()

            self.bullet_batch.draw()

            self.effects_batch.draw()

            for wall in self.walls:
                wall.draw()

            pyglet.gl.glPopMatrix()

            self.hud_batch.draw()

            if self.buy_menu:
                self.buy_menu_batch.draw()

            elif self.keys[key.TAB]:
                self.stats_batch.draw()

        else:
            self.pick_sprite.draw()

        self.mouse.draw()


g = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "Shooter 2", resizable=False)

tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_s.connect((HOST, PORT))
ID = int(tcp_s.recv(1024).decode())
MAP = str(tcp_s.recv(1024).decode())

if not os.path.isfile("./res/maps/" + MAP):
    tcp_s.sendall(b"get map")
    m = tcp_s.recv(20000).decode()

    with open("./res/maps/" + MAP, "w") as r:
        r.write(str(m))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # s.connect((HOST, PORT))

    s.bind(('', MY_PORT))

    addr = (HOST, PORT)

    g.load()

    pyglet.app.run()
