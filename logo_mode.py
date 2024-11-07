from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time

import game_framework
import title_mode


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
    image.clip_draw(74, 25, 135, 24, 400, 300, 270, 48)#135, 24, 74, 27
    update_canvas()

def handle_events():
    events = get_events()