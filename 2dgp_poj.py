from pico2d import *
import random

from control_hero import handle_event
from map import *
from character import *
from NPC import *

def reset_world():
    global running
    global character
    global npc_snake
    global world

    running = True
    world = []

    character = Character(200, 200)

    npc_snake = [NPC_snack() for i in range(20)]
    world += npc_snake


def update_world():
    character.update()
    for o in world:
        o.update()



def render_world():
    character.draw()
    for o in world:
        o.draw()
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
    pico2d.update_canvas()

    pico2d.delay(0.01)
