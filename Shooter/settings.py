import pygame as pg
vec = pg.math.Vector2
pg.init()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)

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
PLAYER_HEALTH = 100

BARREL_OFFSET = vec(40, 16)

#Enemy Setting
ENEMY_IMG = "pistol_enemy.png"
ENEMY_SPEED = 800
ENEMY_HIT_RECT = pg.Rect(0, 0, 35, 35)
ENEMY_HEALTH = 100
ENEMY_BULLET_RATE = 2000
AVOID_RADIUS = 50

#Gun Settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 2000
BULLET_LIFETIME = 5000
BULLET_RATE = 150
BULLET_SIZE = [10, 10]
KICKBACK = 200
GUN_SPREAD = 2
BULLET_DMG = 10

#Hud Settings
BAR_LENGHT = 100
BAR_HEIGHT = 20

#Effects
MUZZLE_FLASH = 'muzzleFlash.png'
FLASH_DURATION = 40

#Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
ENEMY_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4
