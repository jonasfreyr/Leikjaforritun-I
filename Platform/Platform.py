import pygame
import tkinter as tk

root = tk.Tk()

class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.wW = root.winfo_screenwidth()
        self.wH = root.winfo_screenheight()

        pygame.mouse.set_visible(False)

        self.FPS = 120
        self.clock = pygame.time.Clock()


        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.floor = self.black
        self.backround = self.white

        self.size = self.wW / 30

        self.x = 30
        self.y = self.wH / 2 - self.size

        self.speed = 5
        self.gravity = 3
        self.speedUP = 0
        self.jumpSpeed = 10
        self.grounded = False

        self.walls = [[0, self.wH / 4 * 3, self.wW, self.wH]]

    def move(self, x):
        for a in self.walls:
            xW = a[0]
            yW = a[1]

            xS = a[2]
            yS = a[3]

            if (self.x + self.size + x > xW and self.y + self.size > yW) and (self.x + x - self.size < xW + xS and self.y - self.size < yW + yS):
                x = 0

            if (self.x + self.size > xW and self.y + self.size + y > yW) and (self.x - self.size < xW + xS and self.y - self.size + y < yW + yS):
                y = 0

        self.x += x
        self.y += y

    def wallRender(self):
        for a in self.walls:
            pygame.draw.rect(self.screen, self.backround, pygame.Rect(a))

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        quit()
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

            if pressed[pygame.K_SPACE]:
                if self.grounded is True:
                    self.speedUP = self.jumpSpeed
                    self.grounded = False

            game.move(self, x)

            game.wallRender(self)

            pygame.draw.rect(self.screen, self.backround, pygame.Rect(self.x, self.y, self.size, self.size))

            pygame.display.update()

            self.clock.tick(self.FPS)

h = game()
h.loop()