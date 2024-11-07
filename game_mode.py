from pico2d import *
import random

import game_framework
import game_world
import title_mode
from character import Character
from map import *
from NPC import *

center_x = screen_width/2
center_y = screen_height/2

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework,quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
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
    game_world.clear()
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