import pygame, random
import tkinter as tk

root = tk.Tk()
pygame.init()

class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.wW = root.winfo_screenwidth()
        self.wH = root.winfo_screenheight()

        self.clock = pygame.time.Clock()
        self.FPS = 120

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
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

        self.walls = [[0, self.wH / 4 * 3, self.wW, self.wH], [100, self.wH / 4 * 3 - 3 * self.size, self.wH / 4 * 3 - 2 * self.size, 20]]
        self.InWalls = []

        self.restart = False

        self.mouseDown = False

        self.point = (800, self.walls[0][1] - self.size - 1, self.size, self.size)

        self.score = 0

        self.time = (0, 0, 0, 10)

        self.TextColor = (255, 255, 255)
        self.fontSize = int(self.size) * 4
        self.font = pygame.font.SysFont("monospace", self.fontSize)

        self.lose = False

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

    def removeWall(self, poss):
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

            if poss[0] >= xW + xS1 and poss[1] >= yW + yS1 and poss[0] <= xW + xS and poss[1] <= yW + yS:
                if a != self.walls[0]:
                    self.walls.remove(a)

    def NewPoint(self):
        x = random.randint(0, self.wW - self.size)
        y = random.randint(0, int(self.walls[0][1]) - self.size)

        self.point = (x, y, self.size, self.size)

    def pointRender(self):
        pygame.draw.rect(self.screen, self.green, pygame.Rect(self.point))

    def scoreRender(self):
        label = self.font.render(str(self.score), 1, self.TextColor)
        self.screen.blit(label, (0, 0))

    def timerRender(self):
        hour = str(self.time[1])
        minit = str(self.time[2])
        sec = str(self.time[3])

        if len(hour) == 1:
            hour = "0" + hour

        if len(minit) == 1:
            minit = "0" + minit

        if len(sec) == 1:
            sec = "0" + sec

        time = hour + ":" + minit + ":" + sec
        label = self.font.render(str(time), 1, self.TextColor)

        width = label.get_width()

        self.screen.blit(label, (self.wW / 2 - width / 2, 0))

    def timerChange(self, x):
        time = self.time

        t0 = time[0]
        t1 = time[1]
        t2 = time[2]

        t3 = time[3] + x

        if t3 < 0:
            t3 = 59
            t2 = time[2] - 1
            if t2 < 0:
                t2 = 59
                t1 = time[1] - 1
                if t1 < 0:
                    t1 = 59
                    t0 = time[0] - 1
                    if t0 <= 0:
                        game.gameOver(self)

        elif t3 >= 60:
            t3 = t3 - 60
            t2 = time[2] + 1
            if t2 >= 60:
                t2 = t2 - 60
                t1 = time[1] + 1
                if t1 >= 60:
                    t1 = t1 - 60
                    t0 = time[0] + 1

        self.time = (t0, t1, t2, t3)

    def gameOver(self):
        self.lose = True
        label = self.font.render("Game Over", 1, self.TextColor)
        self.screen.blit(label, (self.wW / 2 - self.fontSize * 3, self.wH / 2 - (self.fontSize / 2)))

    def loop(self):
        tel = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.KEYUP:
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

            if self.lose != True:
                self.screen.fill(self.floor)

                x = 0
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_d]:
                    x = self.speed

                if pressed[pygame.K_a]:
                    x -= self.speed

                if pressed[pygame.K_SPACE]:
                    if self.grounded is True:
                        self.velocity = -self.jumpSpeed
                        self.grounded = False

                if pygame.key.get_mods() and pygame.KMOD_LSHIFT:
                        self.speed = self.size / 30

                else:
                    self.speed = self.size / 8

                game.move(self, x)

                game.Falling(self)

                if len(self.walls) > 7:
                    self.walls.remove(self.walls[2])

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
                    game.removeWall(self, poss)

                game.pointRender(self)

                p = (self.point[0] + self.size / 2, self.point[1] + self.size / 2)
                if p[0] >= self.x and p[1] >= self.y and p[0] <= self.x + self.size and p[1] <= self.y + self.size:
                    game.NewPoint(self)
                    self.score += 1
                    game.timerChange(self, 5)

                game.scoreRender(self)

                game.timerRender(self)

                if tel == self.FPS:
                    tel = 0
                    game.timerChange(self, -1)

                pygame.draw.rect(self.screen, self.backround, pygame.Rect(self.x, self.y, self.size, self.size))

                pygame.display.update()

                self.clock.tick(self.FPS)

            if self.restart is True:
                break

            tel += 1

while True:
    h = game()
    h.loop()