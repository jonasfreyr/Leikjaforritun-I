import pygame, random, time, sys
from tkinter import *
pygame.init()
wW = 1200
wH = 900


class game:
    def __init__(self,wW,wH,fjoldi):
        self.screen = pygame.display.set_mode((wW, wH))
        pygame.display.set_caption("Blocks")
        self.clock = pygame.time.Clock()
        self.wW = wW
        self.wH = wH
        self.x = self.wW / 2
        self.y = self.wH / 2
        self.done = False
        self.speed = 3
        self.orange = (255, 100, 0)
        self.blue = (0,0,255)
        self.boxes = []
        self.tel = 0
        self.fjoldi = fjoldi
        self.font = pygame.font.SysFont("monospace",50)
        self.gP = False
        self.tap = False
        self.score = 0
        self.blackS = False


    def thing(self,x):
        print(len(self.boxes))
        if self.tel % self.fjoldi == 0:
            pygame.draw.rect(self.screen, self.orange,pygame.Rect(x, -60, 60, 60))
            box = [x, -60]
            self.boxes.append(box)
        for a in range(len(self.boxes)):
            pygame.draw.rect(self.screen,self.orange, pygame.Rect(self.boxes[a][0],self.boxes[a][1],60,60))
            self.boxes[a].append(self.boxes[a][1]+self.speed)
            self.boxes[a].remove(self.boxes[a][1])
        temp = self.boxes
        for a in temp:
            if a[1] > self.wH:
                self.boxes.remove(a)
        self.tel += 1
    def check(self):
        for a in self.boxes:
            x = a[0]
            y = a[1]


            if (self.x + 56 >= x and self.y + 56 >= y) and (self.x <= x + 56 and self.y <= y + 56):
                game.lost(self)
                break
    def pause(self):
        if self.blackS == False:
            label = self.font.render("Game Paused",1 ,(0,0,0))
        else:
            label = self.font.render("Game Paused", 1, (255, 255, 255))
        self.screen.blit(label,((self.wW / 2) - 120, (self.wH / 2) - 50))
        pygame.display.flip()
        self.clock.tick(60)
    def lost(self):
        self.tap = True
        if self.blackS == False:
            label = self.font.render("You Lost!",1,(0,0,0))
        else:
            label = self.font.render("You Lost!", 1, (255, 255, 255))
        self.screen.blit(label,((self.wW / 2) - 120, (self.wH / 2) - 50))
        pygame.display.flip()
        self.clock.tick(60)
        
    def loop(self):
        Stel = 0
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    quit()
            pressed = pygame.key.get_pressed()
            if self.gP == False and self.tap == False:

                if self.score < 30:
                    self.screen.fill((255, 255, 255))
                elif self.score >= 30:
                    self.blackS = True
                    self.screen.fill((0, 0, 0))


                if self.y > 0:
                    if pressed[pygame.K_UP]: self.y -= self.speed + 1
                if self.y < self.wH - 60:
                    if pressed[pygame.K_DOWN]: self.y += self.speed + 1
                if self.x > 0:
                    if pressed[pygame.K_LEFT]: self.x -= self.speed + 1
                if self.x < self.wW - 60:
                    if pressed[pygame.K_RIGHT]: self.x += self.speed + 1


                pygame.draw.rect(self.screen, self.blue, pygame.Rect(self.x, self.y, 60, 60))

                game.thing(self,random.randint(0,wW-60))

                if Stel % 120 == 0 and Stel != 0:
                    self.score += 1
                Stel += 1

                if self.blackS == False:
                    label = self.font.render(str(self.score), 1, (0, 0, 0))
                else:
                    label = self.font.render(str(self.score), 1, (255, 255, 255))
                self.screen.blit(label, (0, 0))

                pygame.display.flip()
                self.clock.tick(120)
                game.check(self)
            if pressed[pygame.K_r]:
                if self.fjoldi == 40:
                    easy()
                elif self.fjoldi == 30:
                    medium()
                elif self.fjoldi == 20:
                    hard()
                elif self.fjoldi == 10:
                    shard()
            if pressed[pygame.K_ESCAPE] and self.tap == False:

                if self.gP == False:
                    self.gP = True
                elif self.gP == True:
                    self.gP = False
                game.pause(self)
                time.sleep(0.15)



def easy():
    try:
        root.destroy()
    except:
        pass
    h = game(wW,wH,40)
    h.loop()
def medium():
    try:
        root.destroy()
    except:
        pass
    h = game(wW, wH, 30)
    h.loop()
def hard():
    try:
        root.destroy()
    except:
        pass
    h = game(wW, wH, 20)
    h.loop()
def shard():
    try:
        root.destroy()
    except:
        pass

    h = game(wW, wH, 10)
    h.loop()

root = Tk()
button_1 = Button(root, text=" Easy ", command=easy)
button_2 = Button(root, text=" Medium ", command=medium)
button_3 = Button(root, text=" Hard ", command=hard)
button_4 = Button(root, text=" Superhard ",command = shard)


button_1.grid(row = 1,column = 1)
button_2.grid(row = 1,column = 2)
button_3.grid(row = 1,column = 3)
button_4.grid(row = 1,column = 4)
root.mainloop()
