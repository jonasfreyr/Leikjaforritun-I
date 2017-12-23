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

        self.bulletLength = 10
        self.bulletWidth = 1
        self.bulletSpeed = 7

        #[[300, 0], 10, 20]

        self.enemySize = 10
        self.eLife = 20
        self.eSpeed = 2
        self.enemySpawn = 60

        self.Psize = 3

        self.ene = True

        self.fontSize = 50
        self.font = pygame.font.SysFont("monospace", self.fontSize)

        game.restart(self)

    def restart(self):
        self.gP = False
        self.lose = False

        self.enemies = []

        self.shots = []

        self.x = int(self.wW / 2)
        self.y = int(self.wH / 2)

        self.score = 0
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
            x = random.randint(-50, 0 - self.enemySize)
            y = random.randint(0, self.wH)

        elif side == 2:
            x = random.randint(0, self.wW)
            y = random.randint(self.wH + self.enemySize, self.wH + 50)

        elif side == 3:
            x = random.randint(self.wW + self.enemySize, self.wW + 50)
            y = random.randint(0, self.wH)

        e = [[x, y], self.enemySize, self.eLife]

        #print("E:", e)

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
            life = a[2]

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

            #print("X1:", x1, "   Y1:", y1)
            #time.sleep(3)

            for b in self.enemies:
                x2 = b[0][0]
                y2 = b[0][1]

                size2 = b[1]
 #               print("B:", b)
                #time.sleep(3)
                #if (x + x1) > :
                if int(x + x1 + size) == int(x2 + (size2)) and int(y + y1 + size) == int(y2 + (size2)):
                    y1 = 0
                    x1 = 0

            e = [[x + x1, y + y1], size, life]

            self.enemies.insert(tel, e)
            self.enemies.remove(a)
            #print(self.enemies)
            #time.sleep(3)
            tel += 1

    def checkP(self):
        for a in self.enemies:
            x = a[0][0]
            y = a[0][1]

            size = a[1]

            vector1 = []
            vector1.append(x - self.x)
            vector1.append(y - self.y)

            vector2 = []
            vector2.append(x - self.x)
            vector2.append(y + size - self.y)

            if float(self.size) > math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)) or float(self.size) > math.sqrt(math.pow(vector2[0], 2) + math.pow(vector2[1], 2)):
                game.tap(self)

    def checkE(self):
        #[[x, y], self.enemySize, self.eLife]
        # [[x1, y1], [x2, x2], (v1, v2)]
        temps = self.shots
        for a in temps:
            p1 = a[0]

            temp = self.enemies
            tel = 0
            for b in temp:
                x = b[0][0]
                y = b[0][1]

                size = b[1]
                life = b[2]

                if p1[0] > x - size / 2 and p1[0] < x + size / 2 and p1[1] > y and p1[1] < y + size:
                    self.shots.remove(a)

                    e = [[x, y], size, life - 1]
                    #print("E:", e)
                    #print("B:", b)
                    #time.sleep(3)
                    self.enemies.remove(b)

                    if life -1 != 0:
                        self.enemies.insert(tel, e)

                    else:
                        self.score += 1
                    break

                tel += 1

    def tap(self):
        self.lose = True
        label = self.font.render("Game Over", 1, self.color)
        self.screen.blit(label, (self.wW / 2 - self.fontSize * 3, self.wH / 2 - (self.fontSize / 2)))

    def loop(self):
        tel = self.gunFirerate
        telE = self.enemySpawn
        while True:
            #print("Ls:", len(self.shots))
            #print("Le:", len(self.enemies))

            #for a in self.enemies:
             #   print(a[2])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            poss = pygame.mouse.get_pos()
            mpressed = pygame.mouse.get_pressed()
            pressed = pygame.key.get_pressed()

            if self.gP == False and self.lose == False:
                self.screen.fill(self.Scolor)

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

                pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.size)

                game.gunRender(self,poss)

                game.shots(self)

                if telE >= self.enemySpawn and self.ene == True and len(self.enemies) < 100:
                    game.Newenemy(self)
                    telE = 0

                tel += 1
                telE += 1

                game.enemy(self)

                game.checkP(self)

                game.checkE(self)

                game.pointer(self, poss)

                label = self.font.render(str(self.score), 1, self.color)
                self.screen.blit(label, (0, 0))

            if poss[0] < self.screenM:
                pygame.mouse.set_pos([self.screenM, poss[1]])
            if poss[0] > self.wW - self.screenM:
                pygame.mouse.set_pos(self.wW - self.screenM, poss[1])
            if poss[1] < self.screenM:
                pygame.mouse.set_pos([poss[0], self.screenM])
            if poss[1] > self.wH - self.screenM:
                pygame.mouse.set_pos([poss[0], self.wH - self.screenM])

            if pressed[pygame.K_r]:
                game.restart(self)

            pygame.display.flip()
            self.clock.tick(self.FPS)



H = game()
H.loop()