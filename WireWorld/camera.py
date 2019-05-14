import pygame as pg
from settings import *

def collide_rect(one, two):
    return one.rect.colliderect(two.rect)

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        mouse = pg.mouse.get_pos()
        self.x = mouse[0]
        self.y = mouse[1]

class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, camera_width, camera_height)
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def update(self):
        if self.x >= camera_width / 2  and self.x < ww - camera_width / 2:
            self.rect.centerx = self.x

        else:
            self.x = self.rect.centerx

        if self.y > camera_height / 2 and self.y < wh - camera_height / 2:
            self.rect.centery = self.y

        else:
            self.y = self.rect.centery

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def apply_mouse_rect(self, rect):
        tops = [-self.camera.topleft[0], -self.camera.topleft[1]]
        return rect.move(tops)

    def update(self, target):
        x = -target.rect.centerx + int(camera_width / 2)
        y = -target.rect.centery + int(camera_height / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - camera_width), x)
        y = max(-(self.height - camera_height), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
