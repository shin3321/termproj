from pico2d import *
import random

import game_world
from character import Character
from map import *
from NPC import *

center_x = screen_width/2
center_y = screen_height/2

def handle_event():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
           character.handle_event(event)

def init():
    global Running
    global character


    Running = True

    character = Character(screen_width // 2, screen_height // 2)
    npc_snake = NPC_snack()
    npc_bat = NPC_bat()

    game_world.add_obj(character, 0)
    game_world.add_obj(npc_snake, 0)
    game_world.add_obj(npc_bat, 0)

def finish():
    pass


def update():
    #character.update()
    game_world.update(character.x, character.y)


def draw():
    clear_canvas()
    #character.draw()
    game_world.render()
    update_canvas()
    pass