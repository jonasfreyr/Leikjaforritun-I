import pygame, random

class game:
    def __init__(self):
        self.wW = 1200
        self.wH = 900

        self.screen = pygame.display.set_mode((self.wW, self.wH))
        self.Scolor = (255, 255, 255)

        self.color = (0, 0, 0)

        self.FPS = 240
        self.clock = pygame.time.Clock()

        self.width = 10
        self.height = 50

        self.sizeB = 15

        self.speed = 2
        self.speedBall = 1.5

        x1 = random.choice([-self.speedBall, self.speedBall])
        y1 = random.choice([-self.speedBall, self.speedBall])

        self.ballVector = (x1, y1)

        self.xB = self.wW / 2
        self.yB = self.wH / 2

        self.x1 = self.wW / 10
        self.y1 = self.wH / 2 - self.height / 2

        self.x2 = self.wW / 10 * 9
        self.y2 = self.wH / 2 - self.height / 2

        self.restart = False

    def drawPlayers(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x1, self.y1, self.width, self.height))
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x2, self.y2, self.width, self.height))

    def movePlayer(self, y, P):
        if P == 1:
            if self.y1 + y > 0 and self.y1 + y + self.height< self.wH:
                self.y1 += y

        elif P == 2:
            if self.y2 + y > 0 and self.y2 + y + self.height < self.wH:
                self.y2 += y

    def drawBall(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.xB, self.yB, self.sizeB, self.sizeB))

    def moveBall(self):
        self.xB = self.xB + self.ballVector[0]
        self.yB = self.yB + self.ballVector[1]

    def checkBall(self):
        x1 = self.ballVector[0]
        y1 = self.ballVector[1]

        if (self.xB + x1 + self.sizeB > self.x1 and self.yB + self.sizeB > self.y1) and (self.xB + x1 < self.x1 + self.width and self.yB < self.y1 + self.height):
            x1 = -x1

        elif (self.xB + x1 + self.sizeB > self.x2 and self.yB + self.sizeB > self.y2) and (self.xB + x1 < self.x2 + self.width and self.yB < self.y2 + self.height):
            x1 = -x1

        if self.yB + y1 < 0 or self.yB + y1 + self.sizeB > self.wH:
            y1 = -y1

        self.ballVector = (x1, y1)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    quit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        self.restart = True

            self.screen.fill(self.Scolor)

            pygame.draw.line(self.screen, self.color, (self.wW / 2, 0), (self.wW / 2, self.wH), 1)

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                game.movePlayer(self, -self.speed, 1)

            if pressed[pygame.K_s]:
                game.movePlayer(self, self.speed, 1)

            if pressed[pygame.K_UP]:
                game.movePlayer(self, -self.speed, 2)

            if pressed[pygame.K_DOWN]:
                game.movePlayer(self, self.speed, 2)

            game.drawPlayers(self)

            game.checkBall(self)

            game.moveBall(self)

            game.drawBall(self)

            pygame.display.flip()
            self.clock.tick(self.FPS)

            if self.restart is True:
                break

while True:
    h = game()
    h.loop()