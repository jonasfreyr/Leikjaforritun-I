import pygame

pygame.init()

class Pic(pygame.sprite.Sprite):
    def __init__(self, image_file, location, size):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def rotate(img, angle):
    return pygame.transform.rotate(img, angle)

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

        self.speed = 3

        self.size = [16, 35]

        self.ship = Pic("Pictures/spaceship.png" , [self.x, self.y], self.size)
        self.backround = Pic("Pictures/nebula_blue.png", [0, 0], [self.wW, self.wH])

    def move(self):
        self.ship = Pic("Pictures/spaceship.png", [self.x, self.y], self.size)

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.angle += 1 % 360  # Value will reapeat after 359. This prevents angle to overflow.
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    quit()

            self.screen.fill(self.color)
            self.screen.blit(self.backround.image, self.backround.rect)
            self.screen.blit(self.ship.image, self.ship.rect)

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_d]:
                self.ship = rotate(self.ship, -90)

            if pressed[pygame.K_d]:
               self.ship = rotate(self.ship, 90)

            if pressed[pygame.K_s]:
                self.y += self.speed

            if pressed[pygame.K_w]:
                self.y -= self.speed

            game.move(self)

            pygame.display.update()
            self.clock.tick(self.FPS)

h = game()
h.loop()