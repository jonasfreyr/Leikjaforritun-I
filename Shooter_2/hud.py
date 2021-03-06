import pyglet
from settings import *

class AmmoText:
    def __init__(self, game, label):
        self.game = game

        self.label = label

    def update(self):
        self.label.text = str(self.game.player.weapons[self.game.player.num].ammo_in_mag) + "/" + str(self.game.player.weapons[self.game.player.num].extra_ammo)

class Health:
    def __init__(self, game, label):
        self.game = game

        self.label = label

    def update(self):
        self.label.text = str(self.game.player.health)


class Logo:
    def __init__(self, pos, sprite, game):
        self.game = game

        self.sprite = sprite

        self.sprite.image.anchor_x = sprite.width

        self.sprite.x = pos.x
        self.sprite.y = pos.y

    def update(self):
        pass

def update_stats(stat, game, ID):
    for label in game.stats_list:
        label.delete()

    game.stats_list = []

    y = WINDOW_HEIGHT / 3 * 2
    l = pyglet.text.Label("Id  Kills  Deaths", x=WINDOW_WIDTH / 2, y=y, batch=game.stats_batch)
    l.anchor_x = "center"
    game.stats_list.append(l)
    try:
        y -= STATS_PADDING
        text = str(ID) + "  " + str(stat[ID]["kills"]) + "  " + str(stat[ID]["deaths"])
        l = pyglet.text.Label(text, x=WINDOW_WIDTH / 2, y=y, batch=game.stats_batch)
        l.anchor_x = "center"
        game.stats_list.append(l)
    except:
        pass

    for id in stat:
        if id != ID:
            y -= STATS_PADDING
            text = str(id) + "  " + str(stat[id]["kills"]) + "  " + str(stat[id]["deaths"])
            l = pyglet.text.Label(text, x=WINDOW_WIDTH / 2, y=y, batch=game.stats_batch)
            l.anchor_x = "center"
            game.stats_list.append(l)