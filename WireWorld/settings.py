ww = 1600
wh = 1600

FPS = 120

camera_width = 800
camera_height = 800
camera_speed = 5

tile_size = 30
grid_width = int(ww / tile_size)
grid_height = int(wh / tile_size)

black = (0, 0, 0)
yellow = (255, 240, 8)
blue = (0, 0, 255)
red = (255, 0, 0)
hover = (255, 240, 8, 128)

states = {
    "none": black,
    "unactivated": yellow,
    "head": blue,
    "tail": red
}