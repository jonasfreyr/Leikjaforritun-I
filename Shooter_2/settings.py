from vector import *

# Game
FPS = 120
WINDOW_WIDTH = int(1920 / 1.5)
WINDOW_HEIGHT = int(1080 / 1.5)

TILESIZE = 64

MAP = "map1.tmx"

# Hud
FONT_SIZE = 30

# Player
PLAYER_SPEED = 300
PLAYER_IMAGES = {'pistol': "pistol.png", 'shotgun': "shotgun.png", 'rifle': "rifle.png"}
PLAYER_HIT_BOX = Rect(0, 0, TILESIZE * 0.6, TILESIZE * 0.6)

# Crosshair
CROSSHAIR_IMG = "crosshair.png"
CROSSHAIR_HEIGHT = 100
CROSSHAIR_WIDTH = 100

# Grenade
GRENADE_IMG = "grenade.png"
GRENADE_SIZE = Vector(30, 30)
GRENADE_STARTING_VEL = Vector(400, 0)
GRENADE_SLOWDOWN = Vector(200, 0)

# Bullet
BULLET_IMG = "bullet.png"

# Weapon
MUZZLE_FLASH_IMG = "muzzleFlash.png"
MUZZLE_FLASH_LIFESPAWN = 0.05
MUZZLE_FLASH_SIZE = Vector(80, 40)
MUZZLE_OFFSET = Vector(-5, -10)

WEAPONS_TYPES = {"shotgun": "shotgun", "rifle": "auto", "pistol": "semi-auto"}

WEAPONS = {}
WEAPONS["pistol"] = {'bullet_speed': 2000,
                     'bullet_distance': 420,
                     'rate': 1,
                     'kickback': 200,
                     'spread': 2,
                     'damage': 15,
                     'bullet_size': 0.010,
                     'ammo_clip': 12,
                     'ammo_max': 24,
                     'bullet_count': 1,
                     'detect_radius': 400,
                     'offset': Vector(35, -11),
                     'img_size': Vector(TILESIZE, TILESIZE),
                     'img_offset': Vector(5, 5)
                     }

WEAPONS['shotgun'] = {'bullet_speed': 2000,
                     'bullet_distance': 300,
                     'rate': 1.2,
                     'kickback': 800,
                     'spread': 20,
                     'damage': 5,
                     'bullet_size': 0.010,
                     'ammo_clip': 8,
                     'ammo_max': 16,
                     'bullet_count': 20,
                     'detect_radius': 400,
                     'offset': Vector(47, -11),
                     'img_size': Vector(TILESIZE * 1.2, TILESIZE),
                     'img_offset': Vector(10, 5)
                    }

WEAPONS['rifle'] = {'bullet_speed': 2000,
                     'bullet_distance': 800,
                     'rate': 0.15,
                     'kickback': 500,
                     'spread': [0, 1, -2, 5, 10, 7, 5, 3, 0, -3, -6, -10, -6, -4, 2, 0, 0, 0, 5, 10, 7, 5, 3, 0, -3, -6, -10, -6, -4, 2],
                     'damage': 20,
                     'bullet_size': 0.010,
                     'ammo_clip': 30,
                     'ammo_max': 60,
                     'bullet_count': 1,
                     'detect_radius': 600,
                     'offset': Vector(47, -11),
                     'img_size': Vector(TILESIZE * 1.2, TILESIZE),
                     'img_offset': Vector(10, 5)
                    }