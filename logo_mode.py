from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time

import game_framework
import title_mode

screen_width, screen_height = 1200, 800
center_x = screen_width/2
center_y = screen_height/2

def init():
    global image
    global running
    global logo_start_time
    image = load_image('img/Miscellaneous.png')  # 196 81
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 5, 5, center_x, center_y, screen_width, screen_height)
    image.clip_draw(74, 25, 135, 24, center_x, center_y, 540, 96)#135, 24, 74, 27
    update_canvas()

def handle_events():
    events = get_events()