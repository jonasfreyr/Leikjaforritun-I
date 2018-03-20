from settings import *

screen = pg.display.set_mode((WIDTH, HEIGHT))

rect = pg.Rect(WIDTH / 2, HEIGHT / 2, 60, 60)

while True:
    pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
            quit()

        if pressed[0] == 1 and event.type == pg.MOUSEBUTTONUP:
            print("tat")
            if pos[0] > rect.x and pos[0] < rect.x + rect.width and pos[1] > rect.y and pos[1] < rect.y + rect.height:
                print("asf")

    screen.fill(0)

    pg.draw.rect(screen, (255, 255, 255), rect)

    pg.display.flip()