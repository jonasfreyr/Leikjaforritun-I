from settings import *


def draw_text(screen, text, font_name, size, color, x, y, align="nw"):
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

    screen.blit(text_surface, text_rect)

    return text_rect


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


def draw_armor_health(surf, x, y, pct):
    if pct < 0:
        pct = 0

    fill = pct * BAR_LENGHT
    outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

    col = BLUE

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def tab(surf, dim, hud_font, Ekills, Akills, E, A):
    surf.blit(dim, (0, 0))

    draw_text(surf, 'Enemies: {}'.format(E), hud_font, 30, WHITE, WIDTH / 2, HEIGHT / 2, align="center")

    draw_text(surf, 'Enemies Killed: {}'.format(Ekills), hud_font, 30, WHITE, WIDTH / 2, HEIGHT / 2 + 30, align="center")

    draw_text(surf, 'Ally: {}'.format(A), hud_font, 30, WHITE, WIDTH / 2, HEIGHT / 2 + 60, align="center")

    draw_text(surf, 'Ally Killed: {}'.format(Akills), hud_font, 30, WHITE, WIDTH / 2, HEIGHT / 2 + 90, align="center")