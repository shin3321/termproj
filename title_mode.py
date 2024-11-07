from pico2d import *
import game_framework
import game_mode


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

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(game_mode)
def draw():
    clear_canvas()
    image.clip_draw(53, 51, 196, 81,400,300, 392,  162)#53, 51 196, 81
    update_canvas()