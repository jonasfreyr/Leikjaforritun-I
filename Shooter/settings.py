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
NIGHT_COLOR = (10, 10, 10)

BGROUND = DARKGREY
PLCOLOR = WHITE

#Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 200

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
PLAYER_IMAGES = {'pistol': "pistol.png", 'shotgun': "shotgun.png", 'rifle': "rifle.png"}
BARREL_OFFSET = vec(40, 16)

#Images Sizes
IMAGES_SIZES = {'pistol': [TILESIZE, TILESIZE], 'shotgun': [TILESIZE + 10, TILESIZE - 5], 'rifle': [TILESIZE + 10, TILESIZE - 5]}

#Enemy Setting
ENEMY_IMAGES = {'pistol': "pistol_enemy.png", 'shotgun': "shotgun_enemy.png", 'rifle': "rifle_enemy.png"}
ENEMY_IMG = "pistol_enemy.png"
ENEMY_SPEED = 800
ENEMY_HIT_RECT = pg.Rect(0, 0, 35, 35)
ENEMY_HEALTH = 100
ENEMY_BULLET_RATE = 2000
AVOID_RADIUS = 50
DETECT_RADIUS = 400

#Weapon Settings
BULLET_IMG = 'bullet.png'

WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 450,
                     'rate': 500,
                     'kickback': 200,
                     'spread': 2,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'ammo_clip': 12,
                     'ammo_max': 24,
                     'bullet_count': 1
                     }

WEAPONS['shotgun'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 400,
                     'rate':1200,
                     'kickback': 800,
                     'spread': 20,
                     'damage': 5,
                     'bullet_size': 'sm',
                     'ammo_clip': 8,
                     'ammo_max': 16,
                     'bullet_count': 20
                    }

WEAPONS['rifle'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 600,
                     'rate': 150,
                     'kickback': 500,
                     'spread': 5,
                     'damage': 15,
                     'bullet_size': 'lg',
                     'ammo_clip': 30,
                     'ammo_max': 60,
                     'bullet_count': 1
                    }


BULLET_SIZE = [10, 10]

#Hud Settings
BAR_LENGHT = 100
BAR_HEIGHT = 20

#Effects
MUZZLE_FLASH = 'muzzleFlash.png'
FLASH_DURATION = 40

LIGHT_MASK = 'light_350_med.png'
LIGHT_RADIUS = (500, 500)

BLOOD_SPLAT = "blood.png"

#Layers
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
ENEMY_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4

#Items
ITEM_IMAGES = {'Health': 'health_pack.png',
               "Ammo_box": "Ammo-Box-Green.png",
               'shotgun': 'shotgun_item.png',
               'rifle': 'rifle_item.png'
               }
ITEM_SIZES = {'Health': [24, 24], "Ammo_box": [45, 45], 'shotgun': [64, 20], 'rifle': [64, 20]}
HEALTH_PACK_AMOUNT = 50
BOB_RANGE = 10
BOB_SPEED = 0.1

#Sounds
BG_MUSIC = 'Interloper.mp3'

PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']

ENEMY_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']

WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'rifle': ['rifle.wav']
                 }

EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'ammo_pickup': 'small_caliber_shot_gun_cock.wav'}