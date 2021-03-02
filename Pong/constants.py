import pygame, random
from os import path

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

PLAYER_DIMENSIONS = (5, 90)
PLAYER_SPEED = 2
PLAYER_PIXLES_FROM_SIDE = 20

BALL_SIZE = 15
BALL_SPEED = 1.5
MAX_Y_SPEED = 1.7
MAX_ANGLE = 45

BACKGROUND_COLOR = (0, 0, 0)
COLOR = (255, 255, 255)
SERVE_COLOR = (220, 220, 220)
FONT_NAME = 'bahnschrift'
FONT_SIZE = 80
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

HIT_PADDLE_SOUND_NAME = "paddle.mp3"
HIT_PADDLE_SOUND = pygame.mixer.Sound("Sounds/"+HIT_PADDLE_SOUND_NAME)
HIT_PADDLE_SOUND.set_volume(0.1)

HIT_WALL_SOUND_NAME = "wall.mp3"
HIT_WALL_SOUND = pygame.mixer.Sound("Sounds/"+HIT_WALL_SOUND_NAME)
HIT_WALL_SOUND.set_volume(0.1)

SCORE_SOUND_NAME = "score.mp3"
SCORE_SOUND = pygame.mixer.Sound("Sounds/"+SCORE_SOUND_NAME)
SCORE_SOUND.set_volume(0.1)