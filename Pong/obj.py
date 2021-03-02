from constants import *
from vector import Vector
import pygame, random

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(FONT, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)

    screen.blit(text_surface, text_rect)

class Player:
    def __init__(self, x, y, screen):
        self.pos = Vector(x, y)
        self.vel = Vector()

        self.screen = screen

    def move(self, x, y):
        self.vel.x += x

        if not (self.pos.y + y < 0 or self.pos.y + y + PLAYER_DIMENSIONS[1] > WINDOW_HEIGHT):
            self.vel.y += y

    def check_ball(self, ball):
        if (ball.pos.x + BALL_SIZE > self.pos.x and ball.pos.y + BALL_SIZE > self.pos.y) and (
                    ball.pos.x < self.pos.x + PLAYER_DIMENSIONS[0] and ball.pos.y < self.pos.y + PLAYER_DIMENSIONS[1]):

            magnintute = ball.vel.magnitude
            ball.vel += (self.vel * 0.4)
            ball.vel.set_length(magnintute)
            return True

        return False

    def update(self):
        self.pos += self.vel

        self.vel *= 0

    def draw(self):
        pygame.draw.rect(self.screen, COLOR, pygame.Rect(self.pos.x, self.pos.y, PLAYER_DIMENSIONS[0], PLAYER_DIMENSIONS[1]))


class Ball:
    def __init__(self, x, y, screen):
        self.pos = Vector(x, y)
        self.vel = Vector()

        self.screen = screen

    def update(self):
        self.pos += self.vel

        # Needs work
        # print(abs(self.vel.angle_to(Vector(1, 0))))
        if 180 - MAX_ANGLE > abs(self.vel.angle_to(Vector(1, 0))) > MAX_ANGLE:
            if self.vel.get_angle() < 0:
                # print("Neg")
                self.vel = self.vel.rotate(-MAX_ANGLE)
            else:
                # print("Pos")
                self.vel = self.vel.rotate(MAX_ANGLE)

    def draw(self):
        pygame.draw.rect(self.screen, COLOR, pygame.Rect(self.pos.x, self.pos.y, BALL_SIZE, BALL_SIZE))