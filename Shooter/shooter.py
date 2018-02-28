import pygame as pg
from settings import *
from sprites import *
from os import path
from tilemap import *

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0

    fill = pct * BAR_LENGHT
    outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN

    elif pct > 0.3:
        col = YELLOW

    else:
        col = RED

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Shooter")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.gp = False
        pg.key.set_repeat(500, 100)

    def quit(self):
        quit()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        self.map = Map(path.join(map_folder, 'map2.txt'))

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_PISTOL)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, [TILESIZE, TILESIZE])

        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, [TILESIZE, TILESIZE])

        self.enemy_img = pg.image.load(path.join(img_folder, ENEMY_IMG)).convert_alpha()
        self.enemy_img = pg.transform.scale(self.enemy_img, [TILESIZE, TILESIZE])

        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, BULLET_SIZE)

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)

                elif tile == 'P':
                    self.player = Player(self, col, row)

                elif tile == "E":
                    Enemy(self, col, row)

            self.camera = Camera(self.map.width, self.map.height)

        self.loop()

    def loop(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.gp == False:
                self.update()
            self.draw()

            self.clock.tick(FPS)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                self.quit()

            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    self.gp = not self.gp

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.bullets, collide_hit_rect, collide_hit_rect)
        for hit in hits:
            self.player.health -= BULLET_DMG

            print(self.player.health)

            if self.player.health <= 0:
                self.running = False

        if hits:
            self.player.vel = vec(0, 0)

        for a in self.enemies:
            hits = pg.sprite.spritecollide(a, self.bullets, True, collide_hit_rect)
            for hit in hits:
                a.health -= BULLET_DMG
                a.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGROUND)
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        self.screen.blit(FONT.render(str(round(self.clock.get_fps(), 2)), 1, WHITE), (0, 0))

        draw_player_health(self.screen, 10, HEIGHT - BAR_HEIGHT - 10, self.player.health / PLAYER_HEALTH)

        pg.display.flip()

    def go_screen(self):
        pass

    def start_screen(self):
        pass

H = Game()
H.start_screen()
while True:
    H.new()
    H.go_screen()