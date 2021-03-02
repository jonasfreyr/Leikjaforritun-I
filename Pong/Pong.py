from obj import *
import random


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.FPS = FPS
        self.clock = pygame.time.Clock()

        # The inital position of the ball
        x1 = random.choice([-BALL_SPEED, BALL_SPEED])
        y1 = random.choice([-BALL_SPEED, BALL_SPEED])

        # A boolean to see who hit the ball last
        # Used to fix a bug that makes the player hit the ball
        # multiple times.
        self.right = True if x1 < 0 else False

        # Make an instance of the ball
        self.ball = Ball(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, self.screen)
        self.ball.vel.x = x1
        self.ball.vel.y = y1

        # The position of player 1
        x1 = PLAYER_PIXELS_FROM_SIDE
        y1 = WINDOW_HEIGHT / 2 - PLAYER_DIMENSIONS[1] / 2

        # Make an instance of player 1
        player1 = Player(x1, y1, self.screen)

        # The position of player 2
        x2 = WINDOW_WIDTH - PLAYER_PIXELS_FROM_SIDE - PLAYER_DIMENSIONS[0]

        # Make an instance of player 2
        player2 = Player(x2, y1, self.screen)

        # Add the players into a list to be used later
        self.players = [player1, player2]

        # Set all the necessary variables
        self.restart = False
        self.score = [0, 0]
        self.served = False
        self.finished = False

        # print(pygame.font.get_fonts())  # To see all the available fonts

    def reset(self):
        # Reset the ball position
        self.ball.pos.x = WINDOW_WIDTH / 2
        self.ball.pos.y = WINDOW_HEIGHT / 2
        self.served = False

    def checkBall(self):
        '''
        A function to check if the ball collides with something
        '''

        # To check if the player collides with player 1
        if self.players[0].check_ball(self.ball) and self.right:
            self.ball.vel.x *= -1
            self.right = not self.right
            HIT_PADDLE_SOUND.play()

        # To check if the player collides with player 2
        elif self.players[1].check_ball(self.ball) and not self.right:
            self.ball.vel.x *= -1
            self.right = not self.right
            HIT_PADDLE_SOUND.play()

        # If the ball collides with the wall
        if self.ball.pos.y < 0 or self.ball.pos.y + BALL_SIZE > WINDOW_HEIGHT:
            self.ball.vel.y *= -1
            HIT_WALL_SOUND.play()

        # If the ball goes outside the screen
        if self.ball.pos.x < 0:
            self.score[1] += 1
            self.reset()
            SCORE_SOUND.play()

        elif self.ball.pos.x + BALL_SIZE > WINDOW_WIDTH:
            self.score[0] += 1
            self.reset()
            SCORE_SOUND.play()

    def loop(self):
        '''
        The main game loop
        '''
        while True:
            self.events()
            if not self.finished:
                self.update()
            self.draw()

            if self.restart is True:
                break

    def events(self):
        '''
        A function that checks the inputs
        '''

        # For loop to check the KEYUP events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.restart = True

                if not self.finished:
                    if event.key == pygame.K_SPACE:
                        self.served = True

        if not self.finished:
            # Get all the keys being held down
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                self.players[0].move(-PLAYER_SPEED)

            if pressed[pygame.K_s]:
                self.players[0].move(PLAYER_SPEED)

            if pressed[pygame.K_UP]:
                self.players[1].move(-PLAYER_SPEED)

            if pressed[pygame.K_DOWN]:
                self.players[1].move(PLAYER_SPEED)

    def update(self):
        '''
        Updates all the objects

        f.ex Adds the velocity to the position of an object
        '''

        # Get the delta time since the last call
        # Is used to make sure the game plays the same on different Fps
        dt = self.clock.tick(self.FPS)

        self.checkBall()

        if self.served:
            self.ball.update(dt)

        for player in self.players:
            player.update(dt)

        if self.score[0] == 10 or self.score[1] == 10:
            self.finished = True

    def draw(self):
        '''
        Function that draws everything on the screen.
        '''
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.line(self.screen, COLOR, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 1)

        self.drawPlayers()
        self.ball.draw()
        self.draw_text()

        pygame.display.flip()

    def drawPlayers(self):
        '''
        Function that draws all the players
        '''
        for player in self.players:
            player.draw()

    def draw_text(self):
        '''
        Function that draws all the text
        '''

        # If the game is not over and the ball is to be served
        if not self.served and not self.finished:
            draw_text(self.screen, "Serve the ball!", SERVE_COLOR, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5)

        # Draws the scores
        draw_text(self.screen, str(self.score[0]), COLOR, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 10)
        draw_text(self.screen, str(self.score[1]), COLOR, WINDOW_WIDTH / 5*4, WINDOW_HEIGHT / 10)

        # If someone won, draw who won
        if self.finished:
            if self.score[0] == 10:
                draw_text(self.screen, "Left Won!", SERVE_COLOR, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5)

            elif self.score[1] == 10:
                draw_text(self.screen, "Right Won!", SERVE_COLOR, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5)


while True:
    h = Game()
    h.loop()
