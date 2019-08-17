from map import *
from os import path
from objs import *
from pyglet.sprite import Sprite
from pyglet.window import key
from hud import *
from weapons import *
import _thread, socket, site, os, sys

HOST = '192.168.1.188'   # Standard loopback interface address (localhost)
PORT = 65432

conns = {}

players = {}
bullets = {}
grenades = {}

id = 1

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_server_window(object):
    def setupUi(self, server_window):
        server_window.setObjectName("server_window")
        server_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(server_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(80, 70, 331, 451))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 20, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(480, 70, 256, 481))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 530, 331, 20))
        self.lineEdit.setObjectName("lineEdit")
        server_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(server_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        server_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(server_window)
        self.statusbar.setObjectName("statusbar")
        server_window.setStatusBar(self.statusbar)

        self.retranslateUi(server_window)
        QtCore.QMetaObject.connectSlotsByName(server_window)

        self.lineEdit.returnPressed.connect(self.command)

    def retranslateUi(self, server_window):
        _translate = QtCore.QCoreApplication.translate
        server_window.setWindowTitle(_translate("server_window", "MainWindow"))
        self.label.setText(_translate("server_window", "Server"))
        self.label_2.setText(_translate("server_window", "Output"))
        self.label_3.setText(_translate("server_window", "Users"))

    def command(self):
        text = self.lineEdit.text()
        self.lineEdit.clear()

        text = text.split(" ")

        if text[0] == "dc":
            remove_user(int(text[1]))

    def update_output(self, data):
        self.textBrowser.append(data)

    def remove_user(self):
        self.listWidget.clear()
        for id in players:
            self.update_user(id)

    def update_user(self, id):
        self.listWidget.addItem(str(id))

def remove_user(id):
    del conns[id]
    del players[id]
    del bullets[id]
    del grenades[id]
    # ui.remove_user()

def new_client(conn, addr, id):
    # print("Connection started with:", addr)
    msg = "Connection started with:" + str(addr) + " id: " + str(id)
    # ui.update_output(msg)
    print(msg)
    bullets[id] = []
    grenades[id] = []
    while True:
        try:
            if id not in conns:
                conn.sendall(b"dc")
                msg = "Connection ended with:" + str(addr) + " id: " + str(id)
                # ui.update_output(msg)
                print(msg)
                break

            data = conn.recv(262144).decode()

            print(data)
            data = eval(data)


            players[id] = data["player"]
            for bullet in data["bullets"]:
                # print(bullet)
                bullets[id].append(bullet)

            for grenade in data["grenades"]:
                grenades[id].append(grenade)

            # bullets[id] = data["bullets"]
            # grenades[id] = data["grenades"]

        except:
            msg = "Connection ended with:" + str(addr) + " id: " + str(id)
            # ui.update_output(msg)
            print(msg)
            remove_user(id)
            break


        '''
        msg = "Connection ended with:" + str(addr) + " id: " + str(id)
        ui.update_output(msg)
        remove_user(id)
        break
        '''
def socket_func():
    global id
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)

        # _thread.start_new_thread(start_main, ())
        while True:
            conn, addr = s.accept()

            conns[id] = conn

            # ui.update_user(id)
            _thread.start_new_thread(new_client, (conn, addr, id))

            id += 1

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs).__init__(vsync=False)

        self.frame_rate = 1 / 120

        pyglet.clock.schedule_interval(self.update, self.frame_rate)
        pyglet.clock.set_fps_limit(FPS)

        self.set_location(1000, 500)

        self.keys = {key.A: False, key.W: False, key.D: False, key.S: False}

        # self.set_exclusive_mouse(True)

        self.mouse_down = False

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

        for tile_object in self.map.tmx_data.objects:
            pos = Vector(tile_object.x, (self.map.size[1] - tile_object.y - tile_object.height))
            pos.x = pos.x + tile_object.width / 2
            pos.y = pos.y + tile_object.height / 2
            if tile_object.name == "Wall":
                self.walls.append(Wall(tile_object.x, pos.y - tile_object.height / 2, tile_object.width, tile_object.height))

            elif tile_object.name == "Player":
                self.player = Player(pos.x, pos.y, self, tile_object.type)

        self.bullets = []

        self.camera = Camera()

        self.mouse = Mouse(Sprite(self.crosshair_img), self)

        # self.hud_labels.append(Logo(SMOKE_LOGO_POS ,Sprite(self.smoke_logo, batch=self.hud_batch), self))

        #   Ammo Label
        l =  pyglet.text.Label("big lel", x=WINDOW_WIDTH, y=0, batch=self.hud_batch)
        l.anchor_x = "right"
        l.font_size = FONT_SIZE
        self.hud_labels.append(AmmoText(self, l))

        self.target = self.player

    def update(self, dt):
        # print(len(self.bullets))
        # print(len(self.effects))
        # print(len(self.grenades))
        # print(len(self.o_players))
        i_ids = []
        for id in players:
            i_ids.append(id)
            for player in self.o_players:
                if id == player.id:
                    player.rot = players[id]["rot"]
                    player.pos.x = players[id]["pos"]["x"]
                    player.pos.y = players[id]["pos"]["y"]
                    player.weapon = players[id]["weapon"]
                    break

            else:
                self.o_players.append(
                    Oplayers(id, Vector(players[id]["pos"]["x"], players[id]["pos"]["x"]),
                             players[id]["rot"], players[id]["weapon"], self))

        for player in self.o_players:
            if player.id not in i_ids:
                self.o_players.remove(player)

        temp = bullets
        for id in temp:
            for bullet in temp[id]:
                self.bullets.append(Bullet(bullet["pos"]["x"], bullet["pos"]["y"], bullet["rot"], self.bullet_img, bullet["weapon"], self, False))
                self.effects.append(MuzzleFlash(Vector(bullet["pos"]["x"], bullet["pos"]["y"]), bullet["rot"], self))
                bullets[id].remove(bullet)

        temp = grenades
        for id in temp:
            for grenade in temp[id]:
                Grenade(self, grenade["type"]).throw(Vector(grenade["pos"]["x"], grenade["pos"]["y"]),
                                                     Vector(grenade["vel"]["x"], grenade["vel"]["y"]), grenade["rot"],
                                                     True)
                grenades[id].remove(grenade)


        self.dt = dt


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

        for player in self.o_players:
            player.update()

        tempB = []
        for bullet in self.bullets:
            tempB.append({"pos": {"x": bullet.pos.x, "y": bullet.pos.y}, "rot": bullet.rot, "weapon": bullet.weapon})

        tempG = []
        for grenade in self.grenades:
            if grenade.sent is False or grenade.type == "smoke":
                tempG.append({"pos": {"x": grenade.pos.x, "y": grenade.pos.y}, "exploded": grenade.explode, "type": grenade.type, "opacity": grenade.opacity})
                if grenade.explode:
                    grenade.sent = True

        try:
            tempC = conns
            for id in tempC:
                temp = dict(players)
                del temp[id]



                d = {"players": temp, "bullets": tempB, "grenades": tempG}
                conns[id].sendall(str(d).encode())

        except:
            pass

    def on_draw(self):
        pyglet.clock.tick()

        self.clear()

        pyglet.gl.glPushMatrix()
        self.camera.draw(self.target)
        self.map.draw()
        self.main_batch.draw()
        # self.player.draw()
        for player in self.o_players:
            player.sprite.draw()
        self.bullet_batch.draw()
        self.effects_batch.draw()

        for wall in self.walls:
            wall.draw()

        for grenade in self.grenades:
            grenade.draw_hit_box()

        pyglet.gl.glPopMatrix()

        # self.hud_batch.draw()

        # self.mouse.draw()

g = Game(WINDOW_WIDTH, WINDOW_HEIGHT, "Shooter 2", resizable=False)

g.load()
g.new()

_thread.start_new_thread(socket_func, ())

pyglet.app.run()



'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    server_window = QtWidgets.QMainWindow()
    ui = Ui_server_window()
    
    _thread.start_new_thread(start_game, ())
    ui.setupUi(server_window)
    server_window.show()
    sys.exit(app.exec_())
'''