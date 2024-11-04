from pico2d import *
import random

import game_world
from map import *
from character import *
from NPC import *


def handle_event():
    global running
    global key
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
           character.handle_event(event)

def reset_world():
    global running
    global character

    running = True

    character = Character(screen_width // 2, screen_height // 2)

    npc_snake = NPC_snack()
    npc_bat = NPC_bat()
    game_world.add_obj(npc_snake, 1)
    game_world.add_obj(npc_bat, 1)


def update_world():
    character.update()
    game_world.update()


def render_world():
    clear_canvas()
    character.draw()
    game_world.render()
    update_canvas()
    pass


reset_world()

while running:
    handle_event()

    cx = character.x - screen_width //2
    cy = character.y - screen_height//2

    cx = max(0, min(cx, world_width - screen_width))
    cy = max(0, min(cy, world_height - screen_height))

    draw_background(cx, cy)
    update_world()
    render_world()
    #update_canvas()
    delay(0.001)

close_canvas()