class AmmoText:
    def __init__(self, game, label):
        self.game = game

        self.label = label

    def update(self):
        self.label.text = str(self.game.player.weapon.ammo_in_mag) + "/" + str(self.game.player.weapon.extra_ammo)