import pygame
import tkinter as tk

root = tk.Tk()
pygame.init()

class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.wW = root.winfo_screenwidth()
        self.wH = root.winfo_screenheight()

        self.clock = pygame.time.Clock()

        #pygame.mouse.set_visible(False)

        self.FPS = 120
        self.clock = pygame.time.Clock()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.InvallColor = (100, 100, 100)

        self.floor = self.black
        self.backround = self.white

        self.size = self.wW / 80

        self.x = 100
        self.y = 0

        self.jumpSpeed = self.size / 4
        self.speed = self.size / 8
        self.gravity = self.size / 100
        self.velocity = 0
        self.grounded = False

        self.walls = [[0, self.wH / 4 * 3, self.wW, self.wH], [100, self.wH / 4 * 3 - 3 * self.size, self.wH / 4 * 3 - 2 * self.size, 60]]
        self.InWalls = []

        self.restart = False

        self.mouseDown = False

    def move(self, x):
        for a in self.walls:
            xW = a[0]
            yW = a[1]

            xS = a[2]
            yS = a[3]

            xS1 = 0
            yS1 = 0

            if xS < 0:
                xS1 = xS
                xS = 0


            if yS < 0:
                yS1 = yS
                yS = 0

            if (self.x + self.size + x > xW + xS1 and self.y + self.size > yW + yS1) and (self.x + x < xW + xS and self.y < yW + yS):

                if x > 0 and xS1 == 0:
                    self.x = xW - self.size

                elif x > 0 and xS1 != 0:
                    self.x = xW + xS1 - self.size

                if x < 0:
                    self.x = xW + xS

                x = 0

        self.x += x

    def wallRender(self):
        for a in self.walls:
            pygame.draw.rect(self.screen, self.backround, pygame.Rect(a))

    def Falling(self):
        self.velocity += self.gravity

        for a in self.walls:
            xW = a[0]
            yW = a[1]

            xS = a[2]
            yS = a[3]

            xS1 = 0
            yS1 = 0

            if xS < 0:
                xS1 = xS
                xS = 0

            if yS < 0:
                yS1 = yS
                yS = 0

            if (self.x + self.size > xW + xS1 and self.y + self.size + self.velocity > yW + yS1) and (self.x < xW + xS and self.y + self.velocity < yW + yS):

                if self.velocity < 0:
                    self.y = yW + yS

                else:
                    self.grounded = True



                self.velocity = 0
        if self.velocity > 0:
            self.grounded = False

        self.y += self.velocity

    def InvWallRender(self, a):
        x = a[0]
        y = a[1]

        xS = a[2]
        yS = a[3]

        pygame.draw.rect(self.screen, self.InvallColor, pygame.Rect(x, y, xS, yS))

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        quit()

                    if event.key == pygame.K_r:
                        self.restart = True

                    elif event.key == pygame.K_F1:
                        if self.floor is self.white:
                            self.floor = self.black
                            self.backround = self.white

                        elif self.floor is self.black:
                            self.floor = self.white
                            self.backround = self.black

            self.screen.fill(self.floor)

            x = 0
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                x = self.speed

            if pressed[pygame.K_LEFT]:
                x -= self.speed

            if pressed[pygame.K_UP]:
                if self.grounded is True:
                    self.velocity = -self.jumpSpeed
                    self.grounded = False

            game.move(self, x)

            game.Falling(self)

            game.wallRender(self)

            poss = pygame.mouse.get_pos()
            mpressed = pygame.mouse.get_pressed()
            if mpressed[0] == 1:
                if self.mouseDown is False:
                    self.mouseDown = True
                    self.xW = poss[0]
                    self.yW = poss[1]
                    pygame.mouse.get_rel()
                    self.InWalls.append(self.xW)
                    self.InWalls.append(self.yW)

                try:
                    r1 = self.InWalls[2]
                    r2 = self.InWalls[3]

                    self.InWalls.remove(r1)
                    self.InWalls.remove(r2)

                except:
                    pass

                x = (poss[0] - self.xW)
                y = (poss[1] - self.yW)

                self.InWalls.append(x)
                self.InWalls.append(y)

                game.InvWallRender(self, self.InWalls)

            elif mpressed[0] == 0:
                if self.mouseDown is True:
                    self.mouseDown = False
                    poss1 = pygame.mouse.get_rel()
                    w = [self.xW, self.yW, poss1[0], poss1[1]]
                    self.walls.append(w)
                    self.InWalls = []

            if mpressed[2] == 1:
                temp = self.walls
                for a in temp:
                    xW = a[0]
                    yW = a[1]

                    xS = a[2]
                    yS = a[3]

                    xS1 = 0
                    yS1 = 0

                    if xS < 0:
                        xS1 = xS
                        xS = 0

                    if yS < 0:
                        yS1 = yS
                        yS = 0

                    if (poss[0] > xW + xS1 and poss[1] > yW + yS1 and poss[0] < xW + xS and poss[1] < yW + yS):
                        self.walls.remove(a)

            pygame.draw.rect(self.screen, self.backround, pygame.Rect(self.x, self.y, self.size, self.size))

            pygame.display.update()

            self.clock.tick(self.FPS)

            if self.restart is True:
                break

while True:
    h = game()
    h.loop()