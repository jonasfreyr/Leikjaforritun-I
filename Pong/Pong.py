import pygame

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

        self.speed = 2

        self.x1 = self.wW / 10
        self.y1 = self.wH / 2 - self.height / 2

        self.x2 = self.wW / 10 * 9
        self.y2 = self.wH / 2 - self.height / 2

    def drawPlayers(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x1, self.y1, self.width, self.height))
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x2, self.y2, self.width, self.height))

    def movePlayer(self, y1, P):
        if P == 1:
            self.y1 += y1

        elif P == 2:
            self.y2 += y1


    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    quit()

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

            pygame.display.flip()
            self.clock.tick(self.FPS)

h = game()
h.loop()