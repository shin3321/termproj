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

from stage import Block, Arrow, Ladder, Box

stage_config = {
    1: {
        "npcs": [NPC_snake, NPC_bat],
        "npc_pos":[(300, 150), (600, 250), (800, 350)]
    },
    2: {
        "npcs": [NPC_snail, NPC_mini_frog],
        "npc_positions": [(300, 150), (600, 250), (800, 350)],
    }
}

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

def init(stage):

    global Running

    Running = True
    server.background = Background()
    game_world.add_obj(server.background, 0)

    server.block = Block(world_width, 60, world_width // 2, 10, is_background=True)
    game_world.add_obj(server.block, 0)
    game_world.add_collision_pair('block:hero', server.block, None)
    game_world.add_collision_pair('block:bomb', server.block, None)


    # w, h, xPos, yPos
    block_positions = [(100, 50, 1000, 200), (200, 50, 300, 200), (100, 50, 650, 300)]
    server.blocks = [Block(width, height, x, y) for width, height, x, y in block_positions]

    for block in server.blocks:
        game_world.add_obj(block, 0)
        game_world.add_collision_pair('block:hero', block, None)
        game_world.add_collision_pair('block:bomb', block, None)

    server.boxs = [Box(random.randint(0, 800), random.randint(60, 100)) for _ in range(5)]
    for box in server.boxs:
        game_world.add_obj(box, 0)
        game_world.add_collision_pair('box:whip', box, None)
        game_world.add_collision_pair('bomb:box', None, box)

    ladder_positions = [(900, 100), (200, 100), (550, 200)]
    server.ladders = [Ladder(x, y) for x, y in ladder_positions]
    for ladder in server.ladders:
        game_world.add_obj(ladder, 0)
        game_world.add_collision_pair('ladder:hero', ladder, None)  # 각 사다리에 대해 등록

    server.hero = Character()
    game_world.add_obj(server.hero, 1)
    game_world.add_collision_pair('hero:npc_snake', server.hero, None)
    game_world.add_collision_pair('block:hero', None, server.hero)
    game_world.add_collision_pair('ladder:hero', None, server.hero)
    game_world.add_collision_pair('item:hero', None, server.hero)

    arrow = Arrow()
    game_world.add_obj(arrow, 1)


    # global npc_snake
    # global npc_batd
    # global npc_snail

    init_npcs(stage)

    # npc_snakes = [NPC_snake(random.randint(700, 1600-100), 60) for _ in range(10)]
    # game_world.add_objects(npc_snakes, 0)
    # for npc_snake in npc_snakes:
    #     game_world.add_collision_pair('hero:npc_snake', None, npc_snake)
    #     game_world.add_collision_pair('whip:npc_snake', None, npc_snake)
    #     game_world.add_collision_pair('bomb:npc_snake', None, npc_snake)
    #


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

def init_npcs(stage):
    config = stage_config[stage]

    npcs = config["npcs"]  # 현재 스테이지에서 등장할 NPC 클래스 리스트
    npc_positions = config["npc_pos"]  # NPC 위치 리스트

    server.npcs = []
    for i, pos in enumerate(npc_positions):
        npc_class = npcs[i % len(npcs)]  # NPC 종류 순환
        npc = npc_class(*pos)  # NPC 생성
        server.npcs.append(npc)
        game_world.add_obj(npc, 0)  # 게임 월드에 추가

        # 충돌 그룹 등록
        game_world.add_collision_pair(f'hero:npc_{npc_class.__name__.lower()}', server.hero, npc)
        game_world.add_collision_pair(f'whip:npc_{npc_class.__name__.lower()}', None, npc)


def next_stage(current_stage):
    if current_stage == 1:
        init(2)  # 스테이지 2로 전환
    elif current_stage == 2:
        print("Game Over or Loop to Stage 1")


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