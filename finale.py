from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time
from sdl2 import *

import game_framework

screen_width, screen_height = 1200, 800
center_x = screen_width/2
center_y = screen_height/2

def init():
    global image
    global image2
    global running
    image = load_image('img/Ending.png')  # 196 81
    image2 = load_image('img/Miscellaneous.png')
    running = True


def finish():
    global image
    global image2

    del image
    del image2

def update():
    global running


def draw():# 4,396, 476,241
    clear_canvas()
    image.clip_draw(4,275, 325,230, center_x, center_y, screen_width, screen_height+40)
    image.clip_draw(0, 0, 335, 100, center_x, 30, screen_width+10, 300)
    image2.clip_draw(9, 79, 32, 16, center_x, 350, 128, 64)
    update_canvas()

def is_image2_clicked(mouse_x, mouse_y):
    image_x, image_y = center_x, 350
    image_width, image_height = 128, 64
    left = image_x - image_width // 2
    right = image_x + image_width // 2
    bottom = image_y - image_height // 2
    top = image_y + image_height // 2
    return left <= mouse_x <= right and bottom <= mouse_y <= top

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, screen_height - event.y
            if is_image2_clicked(mouse_x, mouse_y):
                game_framework.quit()
    pass
