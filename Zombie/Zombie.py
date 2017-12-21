import pygame, math, random, time
from fractions import Fraction

pygame.init()

class game:
    def __init__(self):
        self.wW = 1200
        self.wH = 900

        pygame.mouse.set_visible(False)

        self.screenM = 20

        self.screen = pygame.display.set_mode((self.wW, self.wH))

        self.FPS = 120
        self.clock = pygame.time.Clock()

        self.Scolor = (255, 255, 255)
        self.color = (0, 0, 0)

        self.size = 10

        self.speed = 3

        self.gunLength = 20
        self.gunWidth = 3
        self.gunFirerate = 2
        self.gunEndx = 1
        self.gunEndy = 1

        self.x = int(self.wW / 2)
        self.y = int(self.wH / 2)

        self.bulletLength = 10
        self.bulletWidth = 1
        self.bulletSpeed = 7

        self.shots = []

        #[[300, 0], 10, 20]
        self.enemies = []

        self.enemySize = 10
        self.eLife = 20
        self.eSpeed = 2
        self.enemySpawn = 60

        self.Psize = 3

        self.ene = True

    def pointer(self, tuple):
        x = tuple[0]
        y = tuple[1]

        pygame.draw.circle(self.screen, self.color, (x, y), self.Psize)

    def gunRender(self, tuple):
        x = tuple[0]
        y = tuple[1]

        vector = []
        vector.append(x - self.x)
        vector.append(y - self.y)

        lengd = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

        if lengd == 0:
            lengd = 1
        lengd = self.gunLength / lengd

        x1 = vector[0]
        y1 = vector[1]

        x1 = x1 * lengd
        y1 = y1 * lengd

        x = self.x + x1
        y = self.y + y1

        self.gunEndx = x
        self.gunEndy = y

        #print("X:", self.x, "Y:", self.y)
        #print("GX:", self.gunEndx, "GY:", self.gunEndy)

        pygame.draw.line(self.screen, self.color, (self.x,self.y), (x, y), self.gunWidth)

    def shoot(self, tuple):
        #[[x1, y1], [x2, x2], (v1, v2)]
        x = tuple[0]
        y = tuple[1]

        vector = []
        vector.append(x - self.gunEndx)
        vector.append(y - self.gunEndy)

        #print(vector)

        lengd = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

        try:
            lengdp = self.bulletLength / lengd

        except:
            lengdp = 1

        try:
            lengdv = self.bulletSpeed / lengd

        except:
            lengdv = 1

        x1 = vector[0]
        y1 = vector[1]

        x1 = int(x1 * lengdp)
        y1 = int(y1 * lengdp)

        x = self.gunEndx + x1
        y = self.gunEndy + y1

        xv = vector[0] * lengdv
        yv = vector[1] * lengdv

        vector = [xv, yv]

        s = [[self.gunEndx, self.gunEndy], [x, y], vector]

        self.shots.append(s)

    def shots(self):
        for a in range(len(self.shots)):
            p1 = self.shots[a][0]
            p2 = self.shots[a][1]

            #print("P1:", p1, "P2:", p2)

            pygame.draw.line(self.screen, self.color,p1, p2, self.bulletWidth)

            p11 = [p1[0] + self.shots[a][2][0], p1[1] + self.shots[a][2][1]]
            p22 = [p2[0] + self.shots[a][2][0], p2[1] + self.shots[a][2][1]]

            self.shots[a].insert(0, p11)
            self.shots[a].remove(p1)
            self.shots[a].insert(1, p22)
            self.shots[a].remove(p2)

        temp = self.shots
        for a in temp:
            if a[0][0] < 0 or a[0][0] > self.wW or a[0][1] < 0 or a[0][1] > self.wH:
                self.shots.remove(a)

    def Newenemy(self):
        side = random.randint(0, 3)

        if side == 0:
            x = random.randint(0, self.wW)
            y = random.randint(-50, 0 - self.enemySize)

        elif side == 1:
            x = random.randint(0, self.wW)
            y = random.randint(-50, 0 - self.enemySize)

        elif side == 2:
            x = random.randint(0, self.wW)
            y = random.randint(-50, 0 - self.enemySize)

        elif side == 3:
            x = random.randint(0, self.wW)
            y = random.randint(-50, 0 - self.enemySize)

        e = [[x, y], self.enemySize, self.eLife]

        self.enemies.append(e)

    def enemy(self):
        for a in range(len(self.enemies)):
            x = self.enemies[a][0][0]
            y = self.enemies[a][0][1]

            size = self.enemies[a][1]

            #pygame.draw.circle(self.screen, self.color, [x, y], size)

            pygame.draw.line(self.screen, self.color,[x, y], [x, y + self.enemySize], size)

        temp = self.enemies
        tel = 0
        for a in temp:
            x = a[0][0]
            y = a[0][1]

            size = a[1]

            vector = []
            vector.append(self.x - x)
            vector.append(self.y - y)

            lengd = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))

            try:
                lengd = self.eSpeed / lengd

            except:
                lengd = 1

            x1 = vector[0]
            y1 = vector[1]

            x1 = (x1 * lengd)
            y1 = (y1 * lengd)

            print("XS:", x1, "   YS:", y1)
            #time.sleep(3)

            for b in self.enemies:
                x2 = b[0][0]
                y2 = b[0][1]

                if x1 > 0 and y1 > 0:
                    
                elif x1 > 0 and y1 < 0:
                elif x1 < 0 and y1 < 0:
                elif x1 < 0 and y1 > 0:


            e = [[x + x1, y + y1], size, self.eLife]
            if y < self.wH + self.enemySize:
                self.enemies.insert(tel, e)
            self.enemies.remove(a)
            #print(self.enemies)
            #time.sleep(3)
            tel += 1

    def loop(self):
        tel = self.gunFirerate
        telE = self.enemySpawn
        while True:
            self.screen.fill(self.Scolor)

            print("Ls:", len(self.shots))
            print("Le:", len(self.enemies))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            poss = pygame.mouse.get_pos()
            mpressed = pygame.mouse.get_pressed()
            pressed = pygame.key.get_pressed()
            if self.y > 0 + self.size:
                if pressed[pygame.K_w]:
                    self.y -= self.speed
            if self.y < self.wH - self.size:
                if pressed[pygame.K_s]:
                    self.y += self.speed
            if self.x > 0 + self.size:
                if pressed[pygame.K_a]:
                    self.x -= self.speed
            if self.x < self.wW - self.size:
                if pressed[pygame.K_d]:
                    self.x += self.speed
            if mpressed[0] == 1 and tel >= self.gunFirerate:
                game.shoot(self, poss)
                tel = 0
            if poss[0] < self.screenM:
                pygame.mouse.set_pos([self.screenM, poss[1]])
            if poss[0] > self.wW - self.screenM:
                pygame.mouse.set_pos(self.wW - self.screenM, poss[1])
            if poss[1] < self.screenM:
                pygame.mouse.set_pos([poss[0], self.screenM])
            if poss[1] > self.wH - self.screenM:
                pygame.mouse.set_pos([poss[0], self.wH - self.screenM])

            pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.size)

            game.pointer(self, poss)

            game.gunRender(self,poss)

            game.shots(self)

            self.clock.tick(self.FPS)

            if telE == self.enemySpawn and self.ene == True:
                game.Newenemy(self)
                telE = 0

            game.enemy(self)

            pygame.display.flip()

            tel += 1
            telE += 1

H = game()
H.loop()