from vector import *

# Game
FPS = 120
WINDOW_WIDTH = int(1920 / 1.5)
WINDOW_HEIGHT = int(1080 / 1.5)

TILESIZE = 64

# Hud
FONT_SIZE = 30

# Player
PLAYER_SPEED = 300
PLAYER_IMAGES = {'pistol': "pistol.png", 'shotgun': "shotgun.png", 'rifle': "rifle.png"}
PLAYER_HIT_BOX = Rect(0, 0, TILESIZE * 0.8, TILESIZE * 0.8)

# Crosshair
CROSSHAIR_IMG = "crosshair.png"
CROSSHAIR_HEIGHT = 100
CROSSHAIR_WIDTH = 100

# Bullet
BULLET_IMG = "bullet.png"

# Weapon
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
                     'offset': Vector(25, -15),
                     'img_size': Vector(TILESIZE, TILESIZE)
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
                     'offset': Vector(35, -15),
                     'img_size': Vector(TILESIZE * 1.2, TILESIZE)
                    }

WEAPONS['rifle'] = {'bullet_speed': 2000,
                     'bullet_distance': 800,
                     'rate': 0.15,
                     'kickback': 500,
                     'spread': [0, 0, 0, 5, 10, 7, 5, 3, 0, -3, -6, -10, -6, -4, 2, 0, 0, 0, 5, 10, 7, 5, 3, 0, -3, -6, -10, -6, -4, 2],
                     'damage': 20,
                     'bullet_size': 0.010,
                     'ammo_clip': 30,
                     'ammo_max': 60,
                     'bullet_count': 1,
                     'detect_radius': 600,
                     'offset': Vector(32, -15),
                     'img_size': Vector(TILESIZE * 1.2, TILESIZE)
                    }