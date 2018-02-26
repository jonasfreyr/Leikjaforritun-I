
import pygame, random

pygame.init()
vec = pygame.math.Vector2

class game:
    def __init__(self):
        self.wW = 800
        self.wH = 600

        self.screen = pygame.display.set_mode((self.wW, self.wH))

        self.color = (255, 255, 255)

        self.clock = pygame.time.Clock()
        self.FPS = 120
 
        self.x = 200
        self.y = 400

        self.vel = vec(0, 0)

        self.speed = 3
        self.rotSpeed = 2

        self.size = [16, 35]

        self.ship = pygame.image.load("Pictures/spaceship.png")
        self.ship = pygame.transform.scale(self.ship, self.size)
        self.ship = pygame.transform.rotate(self.ship, 90)
        self.shipO = self.ship
        self.rect = self.ship.get_rect()

        self.backround = pygame.image.load("Pictures/nebula_blue.png")
        self.backround = pygame.transform.scale(self.backround, [self.wW, self.wH])
        self.Brect = self.backround.get_rect()

        self.missileSize = [20, 20]
        self.missile = pygame.image.load("Pictures/missile.png")
        self.missile = pygame.transform.scale(self.missile, self.missileSize)
        self.missile = pygame.transform.rotate(self.missile, 180)
        self.Mrect = self.missile.get_rect()

        self.astroid = pygame.image.load("Pictures/asteroid.png")
        self.astroid = pygame.transform.scale(self.astroid, [100, 100])
        self.Arect = self.astroid.get_rect()
        self.Arect.center = (self.wW / 2, self.wH / 2)
        self.astroids = []
        self.aSpawnrate = 0.2

        self.angle = 0

        self.missiles = []
        self.missileSpeed = 5

        self.num = 1

        self.gp = False
        self.lose = False

        self.fireRate = 0

    def move(self):
        self.x = self.x + self.vel.x
        self.y = self.y + self.vel.y
        #print(self.vel.x)
        #print(self.vel.y)
        self.rect.center = (self.x, self.y)

    def rotate(self, angle):
        self.angle += angle % 360
        self.ship = pygame.transform.rotate(self.shipO, self.angle) # Value will reapeat after 359. This prevents angle to overflow.
        self.x, self.y = self.rect.center  # Save its current center.
        self.rect = self.ship.get_rect()  # Replace old rect with new rect.
        self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

    def get_keys(self, tel):
        pressed = pygame.key.get_pressed()
        self.vel = vec(0, 0)
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            game.rotate(self, -self.rotSpeed)

        elif pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            game.rotate(self, self.rotSpeed)

        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.vel = vec(self.speed / 2, 0).rotate(-self.angle)

        elif pressed[pygame.K_w] or pressed[pygame.K_UP]:
            self.vel = vec(-self.speed, 0).rotate(-self.angle)

        if pressed[pygame.K_SPACE]:
            if tel >= self.FPS * self.fireRate:
                tel = 0
                game.shoot(self)

        return tel

    def shoot(self):
        a = self.rect.center
        vector = vec(-self.missileSpeed, 0).rotate(-self.angle)
        self.missiles.append([vector, a, self.num, self.angle])

        self.num += 1

    def moveMissiles(self):
        for a in range(len(self.missiles)):
            c = self.missiles[a][1]
            v = self.missiles[a][0]
            #print(v)
            c = [c[0] + v[0], c[1] + v[1]]
            #print(c)
            b = self.missiles[a]

            self.missiles.insert(a, [v, c, self.missiles[a][2], self.missiles[a][3]])
            self.missiles.remove(b)

        temp = self.missiles
        for a in temp:
            c = a[1]
            if c[0] < 0 or c[0] > self.wW or c[1] < 0 or c[1] > self.wH:
                self.missiles.remove(a)

    def renderMissiles(self):
        for a in self.missiles:
            c = self.Mrect
            c.center = a[1]
            an = a[3]
            r = pygame.transform.rotate(self.missile, an)
            #self.ship = pygame.transform.rotate(self.shipO, self.angle)
            self.screen.blit(r, c)
            #pygame.draw.rect(self.screen, (255, 255 ,255), pygame.Rect(a[1].center[0],a[1].center[1], 10, 10))

    def newAstroid(self):
        side = random.randint(0, 3)
        speed = random.randint(0, 2)
        size = random.randint(20, 100)

        if side == 0:
            x = random.randint(0, self.wW)
            y = random.randint(-200, 0 - size)

            angle = random.randint(200, 340)

        elif side == 1:
            x = random.randint(-200, 0 - size)
            y = random.randint(0, self.wH)

            angle = random.randint(-60, 60)

        elif side == 2:
            x = random.randint(0, self.wW)
            y = random.randint(self.wH + size, self.wH + 200)

            angle = random.randint(20, 200)

        elif side == 3:
            x = random.randint(self.wW + size, self.wW + 200)
            y = random.randint(0, self.wH)

            angle = random.randint(140, 240)

        vector = vec(speed, 0).rotate(-angle)
        rect = self.Arect
        rect.center = [x, y]
        self.astroids.append([vector, angle, rect.center, size])

    def renderAstroid(self):
        for a in self.astroids:
            c = self.Arect

            c.center = a[2]

            size = a[3]

            ast = pygame.transform.scale(self.astroid, [size, size])

            self.screen.blit(ast, c)

    def moveAstroid(self):
        for a in range(len(self.astroids)):
            c = self.astroids[a][2]
            v = self.astroids[a][0]
            ang = self.astroids[a][1]
            s = self.astroids[a][3]

            c = [c[0] + v.x, c[1] + v.y]

            #print(c)
            #print("--------")
            b = self.astroids[a]
            self.astroids.insert(a, [v, ang, c, s])
            self.astroids.remove(b)

    def checkP(self):
        for a in self.astroids:
            c = self.Arect

            c.center = a[2]

            #print(self.rect)
            #if ((self.x - size) >= (x2) and (y + size) >= (y2)) and (x + x1 <= x2 + size2 and y <= y2 + size2):

    def loop(self):
        tel = 0
        telA = 0
        brake = False
        while True:
            #print(self.astroids)
            print(self.missiles)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    quit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        self.gp = not self.gp

                    if event.key == pygame.K_r:
                        brake = True

            tel += 1
            telA += 1
            self.screen.fill(self.color)
            self.screen.blit(self.backround, self.Brect)
            game.renderMissiles(self)
            self.screen.blit(self.ship, self.rect)
            game.renderAstroid(self)

            if self.lose != True and self.gp != True:
                tel = game.get_keys(self, tel)

                game.move(self)

                game.moveMissiles(self)

                game.moveAstroid(self)

                game.checkP(self)

                if telA >= self.FPS * self.aSpawnrate and len(self.astroids) < 100:
                    game.newAstroid(self)
                    telA = 0

            if brake == True:
                break

            pygame.display.update()
            self.clock.tick(self.FPS)
while True:
    h = game()
    h.loop()