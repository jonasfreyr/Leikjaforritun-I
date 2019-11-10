from vector import *

def lineLine(x1, y1, x2, y2, x3, y3, x4, y4):
    try:
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

        if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True

        else:
            return False

    except ZeroDivisionError:
        return False

# Game
FPS = 120
WINDOW_WIDTH = int(1920 / 1.5)
WINDOW_HEIGHT = int(1080 / 1.5)

TILESIZE = 64

MAP = "map2.tmx"

HOST = '127.0.0.1'
PORT = 65432
MY_PORT = 65438

# Hud
FONT_SIZE = 30
BUY_MENU_FONT_SIZE = 40
BUY_MENU_PADDING = 20

STATS_PADDING = 20

# Player
PLAYER_SPEED = 300
PLAYER_HIT_BOX = Rect(0, 0, TILESIZE * 0.6, TILESIZE * 0.6)
PLAYER_HEALTH = 100

# Mob
MOB_IMAGE = "zombie.png"
MOB_IMAGE_SIZE = Vector(TILESIZE * 1.2, TILESIZE * 1.2)
MOB_HIT_BOX = Rect(0, 0, TILESIZE * 0.6, TILESIZE * 0.6)
MOB_HEALTH = 100
MOB_ROTATION_SPEED = 5
MOB_SPEED = 100
MOB_NODE_DIST = 10

# Misc
PICK_IMG = "pick.png"
TEAM_DAMAGE_REDUCE = 0.5
LIGHT_IMAGE = "light_350_med.png"

# Crosshair
CROSSHAIR_IMG = "crosshair.png"
CROSSHAIR_HEIGHT = 100
CROSSHAIR_WIDTH = 100

# Grenade
GRENADE_IMG = "grenade.png"
GRENADE_SIZE = Vector(30, 30)
GRENADE_STARTING_VEL = Vector(300, 0)
GRENADE_DISTANCE = 300
GRENADE_HIT_BOX = Rect(0, 0, GRENADE_SIZE.x * 0.6, GRENADE_SIZE.y * 0.6)
GRENADE_DAMAGE_RADIUS = 100
GRENADE_DAMAGE = 65

GRENADE_LOGO = "grenade_logo.png"
GRENADE_LOGO_SIZE = Vector(50, 50)
GRENADE_LOGO_POS = Vector(WINDOW_WIDTH, FONT_SIZE)
GRENADE_LOGO_PADDING = Vector(-5, 5)

EXPLOSION_IMG = "explosion.png"
EXPLOSION_DURATION = 0.01
EXPLOSION_ITEM_SIZE = Vector(96, 96)
EXPLOSION_SIZE = Vector(500, 500)

SMOKE_GRENADE_IMG = "smoke_grenade.png"
SMOKE_GRENADE_SIZE = Vector(120, 60)

SMOKE_IMG = "smoke.png"
SMOKE_DURATION = 10
SMOKE_SIZE = Vector(400, 350)

SMOKE_LOGO = "smoke_logo.png"
SMOKE_LOGO_SIZE = Vector(50, 50)
SMOKE_LOGO_POS = Vector(WINDOW_WIDTH, FONT_SIZE * 2)
SMOKE_LOGO_PADDING = Vector(-5, 5)

# Bullet
BULLET_IMG = "bullet.png"

MUZZLE_FLASH_IMG = "muzzleFlash.png"
MUZZLE_FLASH_LIFESPAWN = 0.05
MUZZLE_FLASH_SIZE = Vector(80, 40)
MUZZLE_OFFSET = Vector(-5, -10)

WEAPONS = {}
WEAPONS["pistol"] = {'bullet_speed': 2000,
                     'bullet_distance': 420,
                     'rate': 0.5,
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
                     'img_offset': Vector(5, 5),
                     'logo_img': "pistol_logo.png",
                     'logo_pos': Vector(WINDOW_WIDTH -130, 0),
                     'logo_size': Vector(70, 40),
                     'primary': False,
                     'knock_back': Vector(500, 0),
                     'type': 'semi-auto',
                     'player_image': 'pistol.png'
                     }

WEAPONS['shotgun'] = {'bullet_speed': 2000,
                     'bullet_distance': 300,
                     'rate': 1.2,
                     'kickback': 800,
                     'spread': 10,
                     'damage': 10,
                     'bullet_size': 0.010,
                     'ammo_clip': 8,
                     'ammo_max': 16,
                     'bullet_count': 20,
                     'detect_radius': 400,
                     'offset': Vector(47, -11),
                     'img_size': Vector(TILESIZE * 1.2, TILESIZE),
                     'img_offset': Vector(10, 5),
                     'logo_img': "shotgun_logo.png",
                     'logo_pos': Vector(WINDOW_WIDTH -100, -25),
                     'logo_size': Vector(170, 110),
                     'primary': True,
                     'knock_back': Vector(800, 0),
                     'type': 'shotgun',
                     'player_image': 'shotgun.png'
                    }

WEAPONS['rifle'] = {'bullet_speed': 2000,
                     'bullet_distance': 800,
                     'rate': 0.15,
                     'kickback': 500,
                     'spread': [0, 1, -2, 5, 10, 7, 5, 3, 0, -3, -6, -10, -6, -4, 2, 0, 0, 0, 5, 10, 7, 5, 3, 0, -3, -6, -10, -6, -4, 2],
                     'damage': 20,
                     'bullet_size': 0.010,
                     'ammo_clip': 30,
                     'ammo_max': 90,
                     'bullet_count': 1,
                     'detect_radius': 600,
                     'offset': Vector(47, -11),
                     'img_size': Vector(TILESIZE * 1.2, TILESIZE),
                     'img_offset': Vector(10, 5),
                     'recovery_time': 1,
                     'logo_img': "ak47_logo.png",
                     'logo_pos': Vector(WINDOW_WIDTH -130, 0),
                     'logo_size': Vector(140, 40),
                     'primary': True,
                     'knock_back': Vector(600, 0),
                     'type': 'auto',
                     'player_image': 'rifle.png'
                    }