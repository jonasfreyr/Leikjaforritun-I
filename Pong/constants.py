import pygame

# Initializes the fonts
pygame.init()

# Sets the title of the window to Pong
pygame.display.set_caption("Pong")

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# Can be changed without affecting the physics
FPS = 60

PLAYER_DIMENSIONS = (5, 90)
PLAYER_SPEED = 0.4

# The amount of pixels from the players and the sides of the screen
PLAYER_PIXELS_FROM_SIDE = 20

BALL_SIZE = 15
BALL_SPEED = 0.5

BACKGROUND_COLOR = (0, 0, 0)
COLOR = (255, 255, 255)

# The serve text color
SERVE_COLOR = (220, 220, 220)

# Font can be changed to some other system font
FONT_NAME = 'bahnschrift'
FONT_SIZE = 80

# Creates the font with the font size
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Relative path to the sound folder
SOUND_FOLDER = "Sounds/"

# Load all the sounds and set the volume to 10% (Was kinda loud)
HIT_PADDLE_SOUND_NAME = "paddle.mp3"
HIT_PADDLE_SOUND = pygame.mixer.Sound(SOUND_FOLDER+HIT_PADDLE_SOUND_NAME)
HIT_PADDLE_SOUND.set_volume(0.1)

HIT_WALL_SOUND_NAME = "wall.mp3"
HIT_WALL_SOUND = pygame.mixer.Sound(SOUND_FOLDER+HIT_WALL_SOUND_NAME)
HIT_WALL_SOUND.set_volume(0.1)

SCORE_SOUND_NAME = "score.mp3"
SCORE_SOUND = pygame.mixer.Sound(SOUND_FOLDER+SCORE_SOUND_NAME)
SCORE_SOUND.set_volume(0.1)
