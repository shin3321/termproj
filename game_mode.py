from random import randint

from pico2d import *
import random

import game_framework
import game_world
import title_mode
from character import Character
from background import *
from NPC import *
import server
import random

from stage import Block, Arrow, Block1, Ladder

center_x = screen_width/2
center_y = screen_height/2

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
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

    server.block = Block()
    game_world.add_obj(server.block, 0)
    game_world.add_collision_pair('block:hero', server.block, None)
    game_world.add_collision_pair('block:bomb', server.block, None)


    # w, h, xPos, yPos
    server.block1 = Block1(100, 50, 600, 200)
    game_world.add_obj(server.block1, 0)
    game_world.add_collision_pair('block1:hero', server.block1, None)

    server.ladder = [Ladder(random.randint(0, 800), random.randint(200, 800)) for _ in range(10)]
    game_world.add_obj(server.ladder, 0)
    for ladder in server.ladder :
        game_world.add_collision_pair('ladder:hero', ladder, None)

    server.hero = Character()
    game_world.add_obj(server.hero, 1)
    game_world.add_collision_pair('hero:npc_snake', server.hero, None)
    game_world.add_collision_pair('block:hero', None, server.hero)
    game_world.add_collision_pair('block1:hero', None, server.hero)
    game_world.add_collision_pair('ladder:hero', None, server.hero)

    arrow = Arrow()
    game_world.add_obj(arrow, 1)


    global npc_snake
    global npc_batd
    global npc_snail

    npc_snakes = [NPC_snake(random.randint(700, 1600-100), 60) for _ in range(10)]
    game_world.add_objects(npc_snakes, 0)
    for npc_snake in npc_snakes:
        game_world.add_collision_pair('hero:npc_snake', None, npc_snake)
        game_world.add_collision_pair('whip:npc_snake', None, npc_snake)
        game_world.add_collision_pair('bomb:npc_snake', None, npc_snake)



    # npc_bats = [NPC_bat(random.randint(100, 1600-100), 60) for _ in range(10)]
    # game_world.add_objects(npc_bats, 0)
    # for npc_bat in npc_bats:
    #     game_world.add_collision_pair('hero:npc_bat', None, npc_bat)
    #     game_world.add_collision_pair('whip,npc_snake', None, npc_bat)
    # game_world.add_collision_pair('hero:npc_bat', server.hero, None)
    #
    # npc_snails = [NPC_snail(random.randint(100, 1600 - 100), 60) for _ in range(10)]
    # game_world.add_objects(npc_snails, 0)
    #
    # for npc_snail in npc_snails:
    #     game_world.add_collision_pair('hero:npc_snail', None, npc_snail)
    #     game_world.add_collision_pair('whip,npc_snake', None, npc_snail)
    # game_world.add_collision_pair('hero:npc_snail', server.hero, None)


def finish():
    game_world.clear()
    pass

def handle_collisions():
    for group, pairs in game_world.collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if game_world.collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def update():
    game_world.update(server.hero.x, server.hero.y)
    handle_collisions()
    delay(0.01)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass