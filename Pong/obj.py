from constants import *
from vector import Vector


def draw_text(screen, text, color, x, y):
    '''
    Draws a text on the desired position
    '''

    # Puts the text into a surface
    text_surface = FONT.render(text, True, color)

    # Creates a rect object at the desired position
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)

    # Adds the text surface into the screen surface on the rect position
    screen.blit(text_surface, text_rect)


class Player:
    '''
    A player object that holds all the necessary methods
    '''
    def __init__(self, x, y, screen):
        '''
        Just takes in the position and the screen surface
        '''
        self.pos = Vector(x, y)

        # Make the velocity 0
        self.vel = Vector()

        self.screen = screen

    def move(self, y):
        '''
        Function that moves the player by y pixels
        '''

        self.vel.y = y

    def check_ball(self, ball):
        '''
        Function that checks if the ball is colliding with the player
        '''
        if (ball.pos.x + BALL_SIZE > self.pos.x and ball.pos.y + BALL_SIZE > self.pos.y) and (
                    ball.pos.x < self.pos.x + PLAYER_DIMENSIONS[0] and ball.pos.y < self.pos.y + PLAYER_DIMENSIONS[1]):

            return True

        return False

    def update(self, dt):
        '''
        Function that updates the position
        '''

        # Multiply by delta time so the game stay the same no matter the Fps
        self.pos += self.vel * dt

        # Checks if the player move too low
        if self.pos.y < 0:
            self.pos.y = 0

        # Check if the player moves to high
        elif self.pos.y + PLAYER_DIMENSIONS[1] > WINDOW_HEIGHT:
            self.pos.y = WINDOW_HEIGHT - PLAYER_DIMENSIONS[1]

        # Reset the velocity so when the player lets go of the key,
        # it will stop moving
        self.vel *= 0

    def draw(self):
        '''
        Function that draws the player
        '''
        pygame.draw.rect(self.screen, COLOR, pygame.Rect(self.pos.x, self.pos.y, PLAYER_DIMENSIONS[0], PLAYER_DIMENSIONS[1]))


class Ball:
    '''
    A ball object that holds all the necessary methods
    '''
    def __init__(self, x, y, screen):
        '''
        Just takes in the position and the screen surface
        '''
        self.pos = Vector(x, y)

        # Make the velocity 0
        self.vel = Vector()

        self.screen = screen

    def update(self, dt):
        '''
        Function that updates the position
        '''

        # Multiply by delta time so the game stay the same no matter the Fps
        self.pos += self.vel * dt

    def draw(self):
        '''
        Function that draws the ball
        '''
        pygame.draw.rect(self.screen, COLOR, pygame.Rect(self.pos.x, self.pos.y, BALL_SIZE, BALL_SIZE))