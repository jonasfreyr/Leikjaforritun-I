import pygame as pg
from settings import *
import random

class Cell(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed, dect_radius, dect_radiusP, forceFood, forcePoison):
        self.groups = game.all_sprites, game.cells
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.pos = vec(x, y)

        self.image = game.arrow.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.rot = 0

        self.detect_radius_food = dect_radius
        self.detect_radius_poison = dect_radiusP

        self.health = 0

        self.speed = speed
        self.force_food = forceFood
        self.force_poison = forcePoison

    def food(self):
        closest = vec(9999, 9999)
        for dot in self.game.food:
            target_dist = dot.pos - self.pos

            if target_dist.length() < closest.length() and target_dist.length() < self.detect_radius_food:
                closest = target_dist
        '''
        closest.scale_to_length(self.speed)

        steer = closest - self.vel
        if steer.length() > self.force:
            steer.scale_to_length(self.force)

        self.acc += steer

        self.vel += self.acc

        self.pos += self.vel

        self.rect.center = self.pos


        self.acc = vec(0, 0)
        '''
        closest.scale_to_length(self.speed)

        steer = closest - self.vel

        rot = steer.angle_to(vec(1, 0))

        self.acc = vec(1, 0).rotate(-rot)

        return steer * self.force_food

    def poison(self):
        closest = vec(999, 999)
        for dot in self.game.poison:
            target_dist = dot.pos - self.pos

            if target_dist.length() < closest.length() and target_dist.length() < self.detect_radius_poison:
                closest = target_dist

        closest.scale_to_length(self.speed)

        steer = closest - self.vel

        rot = steer.angle_to(vec(1, 0))

        self.acc = vec(1, 0).rotate(-rot)

        return steer * self.force_poison

    def update(self):
        self.acc += self.food()

        self.acc -= self.poison()

        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.rect.center = self.pos

        self.rot = self.vel.angle_to(vec(1, 0))

        self.image = pg.transform.rotate(self.game.arrow, self.rot)

        new = random.random()
        print(new)
        if new < 0.0001:
            Cell(self.game, self.pos.x, self.pos.y, self.speed, self.detect_radius_food, self.detect_radius_poison, self.force_food, self.force_poison)

        self.acc = vec(0, 0)

        bol = self.out_of_box()

    def out_of_box(self):
        if WIDTH > self.pos.x > 0 and HEIGHT > self.pos.y > 0:
            return True

        else:
            return False

class Poison(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.poison
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.pos = vec(x, y)

        self.image = pg.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Food(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.food
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.pos = vec(x, y)

        self.image = pg.Surface((5, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos