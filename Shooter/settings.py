import pygame as pg
import tkinter as tk
import glob, os

vec = pg.math.Vector2
pg.init()
root = tk.Tk()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
NIGHT_COLOR = (10, 10, 10)

# Game settings

WIDTH = int(1920 / 1.5)
HEIGHT = int(1080 / 1.5)

FPS = 120
game_folder = os.path.dirname(__file__)
map_folder = os.path.join(game_folder, "maps")
MOPS = glob.glob(map_folder + '/*.tmx')
MAPS = []
BONUS_MAPS = []
for a in MOPS:
    maps = ''
    for b in reversed(a):
        if b.isalpha() or b == "." or b.isdigit() or b == "-" or b == "_":
            maps = b + maps

        else:
            break
    if "bonusmap" in maps:
        BONUS_MAPS.append(maps)

    else:
        MAPS.append(maps)
MAP = MAPS[0]
BONUS_MAP = None

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

CROSSHAIR_IMG = 'crosshair.png'
CROSSHAIR_SIZE = [100, 100]
BLOOD_SCREEN_IMG = 'blood_screen.png'
BLOOD_SCREEN_TIME = 3000

NIGHT_MODE = False
NIGHT_RADIUS = 100

BACKGROUND = "background.png"

# Player Settings
PLAYER_SPEED = 800
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_HEALTH = 100
PLAYER_ARMOR = 50
PLAYER_INVENTORY = ['pistol']
PLAYER_IMAGES = {'pistol': "pistol.png", 'shotgun': "shotgun.png", 'rifle': "rifle.png", "M1": 'rifleL.png', 'uzi': 'uzi.png', "mini": "minigun.png"}
BARREL_OFFSET = vec(40, 16)

# Images Sizes
IMAGES_SIZES = {'uzi': [TILESIZE, TILESIZE], 'pistol': [TILESIZE, TILESIZE], 'shotgun': [TILESIZE + 10, TILESIZE - 5], 'rifle': [TILESIZE + 10, TILESIZE - 5], 'M1': [TILESIZE + 10, TILESIZE - 5], 'mini': [TILESIZE + 10, TILESIZE - 5]}

# Boss
BOSS_HEALTH = 1000
BOSS_IMG = ""

# Enemy Setting
ENEMY_IMAGES = {'pistol': "pistol_enemy.png", 'shotgun': "shotgun_enemy.png", 'rifle': "rifle_enemy.png", "M1": "rifleL_enemy.png", "uzi": "uzi_enemy.png", "mini": "minigun_enemy.png"}
ENEMY_IMG = "pistol_enemy.png"
ENEMY_SPEED = 800
ENEMY_HIT_RECT = pg.Rect(0, 0, 35, 35)
ENEMY_HEALTH = 100
AVOID_RADIUS = 50
ENEMY_ROTATION_SPEED = 5
ENEMY_SPAWNRATE = 2000

# Weapon Settings
BULLET_IMG = 'bullet.png'

WEAPON_TYPES = {
    'shotgun': 'shotgun',
    'pistol': 'pistol',
    'rifle': 'rifle',
    'M1': 'rifle',
    'uzi': 'rifle',
    'mini': 'rifle'

}

WEAPON = []
for a in WEAPON_TYPES:
    WEAPON.append(a)

WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 260,
                     'rate': 500,
                     'kickback': 200,
                     'spread': 2,
                     'damage': 15,
                     'bullet_size': 'lg',
                     'ammo_clip': 12,
                     'ammo_max': 24,
                     'bullet_count': 1,
                     'detect_radius': 400
                     }

WEAPONS['shotgun'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 300,
                     'rate': 1200,
                     'kickback': 800,
                     'spread': 20,
                     'damage': 5,
                     'bullet_size': 'sm',
                     'ammo_clip': 8,
                     'ammo_max': 16,
                     'bullet_count': 20,
                     'detect_radius': 400
                    }

WEAPONS['rifle'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 500,
                     'rate': 150,
                     'kickback': 500,
                     'spread': 5,
                     'damage': 20,
                     'bullet_size': 'lg',
                     'ammo_clip': 30,
                     'ammo_max': 60,
                     'bullet_count': 1,
                     'detect_radius': 600
                    }

WEAPONS['M1'] = {'bullet_speed': 3000,
                     'bullet_lifetime': 800,
                     'rate': 1200,
                     'kickback': 500,
                     'spread': 2,
                     'damage': 40,
                     'bullet_size': 'lg',
                     'ammo_clip': 5,
                     'ammo_max': 15,
                     'bullet_count': 1,
                     'detect_radius': 800
                    }

WEAPONS['uzi'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 300,
                     'rate': 70,
                     'kickback': 200,
                     'spread': 15,
                     'damage': 15,
                     'bullet_size': 'lg',
                     'ammo_clip': 20,
                     'ammo_max': 60,
                     'bullet_count': 1,
                     'detect_radius': 400
                    }

WEAPONS['mini'] = {'bullet_speed': 2000,
                     'bullet_lifetime': 700,
                     'rate': 10,
                     'kickback': 50,
                     'spread': 10,
                     'damage': 20,
                     'bullet_size': 'lg',
                     'ammo_clip': 120,
                     'ammo_max': 240,
                     'bullet_count': 1,
                     'detect_radius': 700
                    }


BULLET_SIZE = [10, 10]

# Hud Settings
BAR_LENGHT = 100
BAR_HEIGHT = 20

WEAPON_NAMES = {
    'rifle': 'AK-47 ',
    'pistol': 'USP',
    'shotgun': 'Mossberg 590',
    'M1': 'M1 Garand',
    'uzi': 'UZI ',
    'mini': 'MINIGUN'

}

# Effects
MUZZLE_FLASH = 'muzzleFlash.png'
FLASH_DURATION = 40

LIGHT_MASK = 'light_350_med.png'
LIGHT_RADIUS = (500, 500)

BLOOD_SPLAT = "blood.png"

# Layers
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
ENEMY_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4

# Items
ITEM_IMAGES = {'Health': 'health_pack.png',
               "Ammo_box": "Ammo-Box-Green.png",
               'shotgun': 'shotgun_item.png',
               'rifle': 'rifle_item.png',
               'armor': 'armor-vest.png',
               'M1': 'M1_item.png',
               'uzi': 'uzi_item.png'
               }
ITEM_SIZES = {'Health': [24, 24], "Ammo_box": [45, 45], 'shotgun': [64, 20], 'rifle': [64, 20], 'armor': [24, 24], 'M1': [64, 20], 'uzi': [40, 20]}
HEALTH_PACK_AMOUNT = 50
BOB_RANGE = 10
BOB_SPEED = 0.1

# Sounds
BG_MUSIC = 'Interloper.mp3'

PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']

ENEMY_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']

WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'rifle': ['rifle.wav'],
                 'M1': ['M1 Garand.wav'],
                 'uzi': ['uzi.wav'],
                 'mini': ['mini.wav']
                 }

OUT_OF_AMMO = 'Dry-Fire-Gun.wav'

EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'ammo_pickup': 'small_caliber_shot_gun_cock.wav',
                  'armor_pickup': 'zipper.wav',
                  'reload': 'reload.wav'
                  }