from pico2d import *

from character import character


def handle_event():
    global running
    global key
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
        #     key = 1
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
        #     key = 2
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
        #     key = 3
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
        #     key = 4
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
        #     key = 5
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
        #     key = 6
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
        #     key = 7
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
        #     key = 8
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:
        #     key = 9
        else:
            character.handle_event(event)