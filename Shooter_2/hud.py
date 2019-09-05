class AmmoText:
    def __init__(self, game, label):
        self.game = game

        self.label = label

    def update(self):
        self.label.text = str(self.game.player.weapon.ammo_in_mag) + "/" + str(self.game.player.weapon.extra_ammo)

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