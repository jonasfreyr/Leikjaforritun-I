import pytmx
import platform
from pytmx.util_pyglet import load_pyglet
import pyglet
from pyglet import image
from pyglet.sprite import Sprite
from settings import *
from vector import Vector
from pytmx import *
import logging

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def preload_img(img):
    return pyglet.image.load("res/img/" + img)

class TiledRenderer(object):
    """
    Super simple way to render a tiled map with pyglet
    no shape drawing yet
    """
    def __init__(self, filename):

        tm = load_pyglet(filename)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.batches = []   # list of batches, e.g. layers
        self.sprites = []   # container for tiles
        self.generate_sprites()

    def draw_rect(self, color, rect, width):
        pass

    def draw_lines(self, color, closed, points, width):
        pass

    def generate_sprites(self):
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        mw = self.tmx_data.width
        mh = self.tmx_data.height - 1
        pixel_height = (mh + 1) * th
        draw_rect = self.draw_rect
        draw_lines = self.draw_lines

        rect_color = (255, 0, 0)
        poly_color = (0, 255, 0)

        for layer in self.tmx_data.visible_layers:
            batch = pyglet.graphics.Batch() # create a new batch
            self.batches.append(batch)      # add the batch to the list
            # draw map tile layers

            if isinstance(layer, TiledTileLayer):

                # iterate over the tiles in the layer
                for x, y, image in layer.tiles():
                    y = mh - y
                    x = x * tw
                    y = y * th
                    sprite = pyglet.sprite.Sprite(
                        image, batch=batch, x=x, y=y
                    )
                    self.sprites.append(sprite)

            # draw object layers
            elif isinstance(layer, TiledObjectGroup):

                # iterate over all the objects in the layer
                for obj in layer:
                    # logger.info(obj)

                    # objects with points are polygons or lines
                    if hasattr(obj, 'points'):
                        draw_lines(poly_color, obj.closed, obj.points, 3)

                    # some object have an image
                    elif obj.image:
                        obj.image.blit(obj.x, pixel_height - obj.y)

                    # draw a rect for everything else
                    else:
                        draw_rect(rect_color,
                                  (obj.x, obj.y, obj.width, obj.height), 3)

            # draw image layers
            elif isinstance(layer, TiledImageLayer):
                if layer.image:
                    x = mw // 2  # centers image
                    y = mh // 2
                    sprite = pyglet.sprite.Sprite(
                        layer.image, batch=batch, x=x, y=y
                    )
                    self.sprites.append(sprite)

    def draw(self):
        for b in self.batches:
            b.draw()

        # self.restore()

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, target):
        self.x = (-target.pos.x - (target.width / 2)) + (WINDOW_WIDTH / 2)
        self.y = (-target.pos.y - (target.height / 2)) + (WINDOW_HEIGHT / 2)
        pyglet.gl.glTranslated(self.x, self.y, 0)
