import pygame as pg

pg.init()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)

BGROUND = DARKGREY
PLCOLOR = WHITE

#Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 300

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

FONTSIZE = int(TILESIZE / 2)
FONT = pg.font.SysFont("monospace", FONTSIZE)

WALL_IMG = 'wall1.png'

#Player Settings
PLAYER_SPEED = 800
PLAYER_MELEE = "melee.png"
PLAYER_FLASHLIGHT = "flashlight.png"
PLAYER_PISTOL = "pistol.png"
PLAYER_SHOTGUN = "shotgun.png"
PLAYER_RIFLE = "rifle.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

#Enemy Setting
ENEMY_IMG = "pistol_enemy.png"
ENEMY_SPEED = 800
ENEMY_HIT_RECT = pg.Rect(0, 0, 35, 35)

#Gun Settings
BULLET_IMG = 'bullet.png'