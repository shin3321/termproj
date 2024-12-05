from pico2d import *
from sdl2.ext import mouse_clicked

import game_framework
import game_mode
screen_width, screen_height = 1200, 800
center_x = screen_width/2
center_y = screen_height/2

def init():
    global image
    image = load_image('img/Miscellaneous.png')
def finish():
    global image
    del image


def update():
    pass

def draw():
    pass
def is_image1_clicked(mouse_x, mouse_y):
    image_x, image_y = center_x, 175
    image_width, image_height = 128, 64
    left = image_x - image_width // 2
    right = image_x + image_width // 2
    bottom = image_y - image_height // 2
    top = image_y + image_height // 2
    return left <= mouse_x <= right and bottom <= mouse_y <= top

def is_image2_clicked(mouse_x, mouse_y):
    image_x, image_y = center_x, 100
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
            if is_image1_clicked(mouse_x, mouse_y):
                game_framework.change_mode(game_mode)
            elif is_image2_clicked(mouse_x, mouse_y):
                game_framework.quit()

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 5, 5, center_x, center_y, screen_width, screen_height )
    image.clip_draw(53, 51, 196, 81,center_x, center_y+50, 784,  324)#53, 51 196, 81
    image.clip_draw(94, 8, 32, 16, center_x, 175, 128, 64)#32, 16// 94,8
    #image.clip_draw(7, 44, 32, 16, center_x, 150, 96, 48)
    image.clip_draw(9, 79, 32, 16, center_x, 100, 128, 64)
    update_canvas()