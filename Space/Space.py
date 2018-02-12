import pygame

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

        self.angle = 0

        self.missiles = []
        self.missileSpeed = 1

        self.num = 1

    def move(self):
        self.x = self.x + self.vel.x
        self.y = self.y + self.vel.y
        #print(self.vel.x)
        #print(self.vel.y)
        self.rect.center = (self.x, self.y)

    def rotate(self, angle):
        self.angle += angle % 360
        self.ship = pygame.transform.rotate(self.shipO, self.angle)
          # Value will reapeat after 359. This prevents angle to overflow.
        self.x, self.y = self.rect.center  # Save its current center.
        self.rect = self.ship.get_rect()  # Replace old rect with new rect.
        self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

    def get_keys(self):
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
            game.shoot(self)

    def shoot(self):
        a = self.Mrect
        a.center = (10, 100)
        print(a)
        self.missiles.append([self.missileSpeed, a, self.num])

        self.num +=1

    def moveMissiles(self):
        temp = self.missiles
        print(temp)
        print("---")
        for a in temp:
            c = a[1]
            c.center = (c.center[0] + self.missileSpeed, c.center[1])
            #print(c)
            self.missiles.remove(a)
            self.missiles.append([self.missileSpeed, c, a[2]])

    def renderMissiles(self):
        for a in self.missiles:
            #print(a)
            self.screen.blit(self.missile, a[1])
            #pygame.draw.rect(self.screen, (255, 255 ,255), pygame.Rect(a[1].center[0],a[1].center[1], 10, 10))


    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    quit()

            self.screen.fill(self.color)
            self.screen.blit(self.backround, self.Brect)
            self.screen.blit(self.ship, self.rect)
            game.renderMissiles(self)

            game.get_keys(self)

            game.move(self)

            game.moveMissiles(self)

            pygame.display.update()
            self.clock.tick(self.FPS)

h = game()
for a in range(6):
    h.shoot()
h.loop()