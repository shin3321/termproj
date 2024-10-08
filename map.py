from pico2d import *

screen_width, screen_height = 1200, 800
world_width, world_height = 2000, 2000
back_wid, back_height = 200, 400



def draw_background(cx, cy):
    for x in range(0, world_width, back_wid):
        background = load_image('img/Dwelling_Tiles.png')
        for y in range(0, world_height, back_height):
            background.clip_draw(0, 644, 508, 892, x - cx, y - cy, back_wid, back_height)

open_canvas(screen_width, screen_height)