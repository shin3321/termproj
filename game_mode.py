from pico2d import *
import random

import game_framework
import game_world
import title_mode
from character import Character
from background import *
from NPC import *
import server

center_x = screen_width/2
center_y = screen_height/2

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework,quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            #game_framework.change_mode(title_mode)
            pass
        else:
           server.hero.handle_event(event)

def init():
    global Running


    Running = True
    server.background = Background()
    game_world.add_obj(server.background, 0)

    server.hero = Character()
    game_world.add_obj(server.hero, 1)

    npc_snake = NPC_snack()
    npc_bat = NPC_bat()
    npc_snail = NPC_snail()

    game_world.add_obj(npc_snake, 0)
    game_world.add_obj(npc_bat, 0)
    game_world.add_obj(npc_snail, 0)

def finish():
    game_world.clear()
    pass


def update():

    game_world.update(server.hero.x, server.hero.y)
    delay(0.05)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass