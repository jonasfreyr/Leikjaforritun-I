import pyglet

def preload_img(img):
    return pyglet.image.load("res/sprites/" + img)

class GameObject:
    def __init__(self, posx, posy, sprite=None):
        self.posx = posx
        self.posy = posy

        self.velx = 0
        self.vely = 0

        if sprite is not None:
            self.sprite = sprite
            self.sprite.x = self.posx
            self.sprite.y = self.posy

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.posx += self.velx * dt
        self.posy += self.vely * dt

        self.sprite.x = self.posx
        self.sprite.y = self.posy