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

        self.angle = 0

        self.missiles = []
        self.missileSpeed = 2

    def move(self):
        self.x = self.x + self.vel.x
        self.y = self.y + self.vel.y
        print(self.vel.x)
        print(self.vel.y)
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
        if pressed[pygame.K_d]:
            game.rotate(self, -self.rotSpeed)

        elif pressed[pygame.K_a]:
            game.rotate(self, self.rotSpeed)

        elif pressed[pygame.K_s]:
            self.vel = vec(self.speed / 2, 0).rotate(-self.angle)

        elif pressed[pygame.K_w]:
            self.vel = vec(-self.speed, 0).rotate(-self.angle)

        if pressed[pygame.K_SPACE]:
            game.shoot(self)

    def shoot(self):
        self.missiles.append(self.rect.top, vec(self.missileSpeed, 0).rotate(-self.angle))

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    quit()

            self.screen.fill(self.color)
            self.screen.blit(self.backround, self.Brect)
            self.screen.blit(self.ship, self.rect)

            game.get_keys(self)

            game.move(self)

            pygame.display.update()
            self.clock.tick(self.FPS)

h = game()
h.loop()