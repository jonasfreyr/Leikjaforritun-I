from obj import *

class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.FPS = 240
        self.clock = pygame.time.Clock()

        x1 = random.choice([-BALL_SPEED, BALL_SPEED])
        y1 = random.choice([-BALL_SPEED, BALL_SPEED])

        self.right = True if x1 < 0 else False

        self.ball = Ball(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, self.screen)
        self.ball.vel.x = x1
        self.ball.vel.y = y1

        x1 = PLAYER_PIXLES_FROM_SIDE
        y1 = WINDOW_HEIGHT / 2 - PLAYER_DIMENSIONS[1] / 2

        player1 = Player(x1, y1, self.screen)

        x2 = WINDOW_WIDTH - PLAYER_PIXLES_FROM_SIDE - PLAYER_DIMENSIONS[0]
        player2 = Player(x2, y1, self.screen)

        self.players = [player1, player2]

        self.restart = False

        self.score = [0, 0]

        self.served = False

        # print(pygame.font.get_fonts())  # To see all the available fonts

        pygame.init()

    def reset(self):
        self.ball.pos.x = WINDOW_WIDTH / 2
        self.ball.pos.y = WINDOW_HEIGHT / 2
        self.served = False

    def checkBall(self):
        if self.players[0].check_ball(self.ball) and self.right:
            self.ball.vel.x *= -1
            self.right = not self.right

        elif self.players[1].check_ball(self.ball) and not self.right:
            self.ball.vel.x *= -1
            self.right = not self.right

        if self.ball.pos.y < 0 or self.ball.pos.y + BALL_SIZE > WINDOW_HEIGHT:
            self.ball.vel.y *= -1

        if self.ball.pos.x < 0:
            self.score[1] += 1
            self.reset()

        elif self.ball.pos.x + BALL_SIZE > WINDOW_WIDTH:
            self.score[0] += 1
            self.reset()

    def loop(self):
        while True:
            self.events()
            self.update()
            self.draw()

            if self.restart is True:
                break

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.restart = True

                if event.key == pygame.K_SPACE:
                    self.served = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.players[0].move(0, -PLAYER_SPEED)

        if pressed[pygame.K_s]:
            self.players[0].move(0, PLAYER_SPEED)

        if pressed[pygame.K_UP]:
            self.players[1].move(0, -PLAYER_SPEED)

        if pressed[pygame.K_DOWN]:
            self.players[1].move(0, PLAYER_SPEED)

    def update(self):
        self.checkBall()

        if self.served:
            self.ball.update()

        for player in self.players:
            player.update()

        self.clock.tick(self.FPS)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.line(self.screen, COLOR, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 1)

        self.drawPlayers()
        self.ball.draw()
        self.draw_text()

        pygame.display.flip()

    def drawPlayers(self):
        for player in self.players:
            player.draw()

    def draw_text(self):
        if not self.served:
            draw_text(self.screen, "Serve the ball!", 80, SERVE_COLOR, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5)

        draw_text(self.screen, str(self.score[0]), 80, COLOR, WINDOW_WIDTH / 5, WINDOW_HEIGHT / 10)
        draw_text(self.screen, str(self.score[1]), 80, COLOR, WINDOW_WIDTH / 5*4, WINDOW_HEIGHT / 10)

while True:
    h = game()
    h.loop()