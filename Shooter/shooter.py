import pygame as pg
from settings import *
from sprites import *
from os import path
from tilemap import *
import random

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
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        pg.display.set_caption("Shooter")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.draw_hit_boxes = False

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)

        self.screen.blit(text_surface, text_rect)

    def quit(self):
        quit()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')

        self.title_font = path.join(img_folder, 'airstrike.ttf')
        self.hud_font = path.join(img_folder, 'conthrax-sb.ttf')

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        #self.player_img = pg.image.load(path.join(img_folder, PLAYER_PISTOL)).convert_alpha()
        #self.player_img = pg.transform.scale(self.player_img, [TILESIZE, TILESIZE])

        self.player_images = {}
        for a in PLAYER_IMAGES:
            p = pg.image.load(path.join(img_folder, PLAYER_IMAGES[a])).convert_alpha()

            p = pg.transform.scale(p, IMAGES_SIZES[a])

            self.player_images[a] = p

        self.enemy_img = pg.image.load(path.join(img_folder, ENEMY_IMG)).convert_alpha()
        self.enemy_img = pg.transform.scale(self.enemy_img, [TILESIZE, TILESIZE])

        self.enemy_images = {}
        for a in ENEMY_IMAGES:
            p = pg.image.load(path.join(img_folder, ENEMY_IMAGES[a])).convert_alpha()

            p = pg.transform.scale(p, IMAGES_SIZES[a])

            self.enemy_images[a] = p

        self.bullet_images = {}
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['lg'] = pg.transform.scale(self.bullet_img, BULLET_SIZE)
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_img, (8, 8))

        self.gun_flash = pg.image.load(path.join(img_folder, MUZZLE_FLASH)).convert_alpha()

        self.blood = pg.image.load(path.join(img_folder, BLOOD_SPLAT)).convert_alpha()
        self.blood = pg.transform.scale(self.blood, (TILESIZE, TILESIZE))

        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))

        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))

                #if weapon == "shotgun":
                s.set_volume(0.3)

                self.weapon_sounds[weapon].append(s)

        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

        self.enemy_hit_sounds = []
        for snd in ENEMY_HIT_SOUNDS:
            self.enemy_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        self.map = TiledMap(path.join(self.map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == "Player":
                self.player = Player(self, obj_center.x, obj_center.y)

            if tile_object.name == "Wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == "Enemy":
                Enemy(self, obj_center.x, obj_center.y, tile_object.type)

            if tile_object.name in ITEM_IMAGES:
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)

        self.gp = False
        self.night = False

        #self.effects_sounds['level_start'].play()

        self.loop()

    def loop(self):
        self.running = True
        #ddpg.mixer.music.play(loops=-1)
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.gp is False:
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

                if event.key == pg.K_r:
                    self.running = False

                if event.key == pg.K_F1:
                    self.draw_hit_boxes = not self.draw_hit_boxes

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "Health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)

            elif hit.type == "Ammo_box":
                hit.kill()
                self.effects_sounds['ammo_pickup'].play()

            elif hit.type in WEAPONS:
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = hit.type

        hits = pg.sprite.spritecollide(self.player, self.bullets, collide_hit_rect, collide_hit_rect)
        for hit in hits:
            #wself.player.health -= WEAPONS[hit.weapon]['damage']

            if self.player.health <= 0:
                self.running = False

        if hits:
            random.choice(self.player_hit_sounds).play()
            self.player.vel = vec(0, 0)

        for a in self.enemies:
            hits = pg.sprite.spritecollide(a, self.bullets, True, collide_hit_rect)
            for hit in hits:
                a.health -= WEAPONS[hit.weapon]['damage']
                a.vel = vec(0, 0)

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)

        self.light_rect.center = self.camera.apply(self.player).center

        self.fog.blit(self.light_mask, self.light_rect)

        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        #self.screen.fill(BGROUND)
        #self.draw_grid()

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.night:
            self.render_fog()

        self.screen.blit(FONT.render(str(round(self.clock.get_fps(), 2)), 1, WHITE), (0, 0))

        draw_player_health(self.screen, 10, HEIGHT - BAR_HEIGHT - 10, self.player.health / PLAYER_HEALTH)

        self.draw_text('Enemies: {}'.format(len(self.enemies)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")

        if self.gp:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        if self.draw_hit_boxes is True:
            self.player.draw_hit_box()

            for a in self.enemies:
                a.draw_hit_box()

            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)

        pg.display.flip()

    def go_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")

        self.draw_text("Retry? y/n", self.title_font, 75, RED, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()

        return self.wait_for_key()

    def wait_for_key(self):
        while True:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                    self.quit()

                if event.type == pg.KEYUP:
                    if event.key == pg.K_y:
                        return False

                    elif event.key == pg.K_n:
                        return True


    def start_screen(self):
        pass

H = Game()
H.start_screen()
while True:
    H.new()
    end = H.go_screen()
    if end is True:
        break