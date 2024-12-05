from random import randint

from pico2d import *
import random
import importlib

import game_framework
import game_world
import title_mode
from character import Character
from background import *
from NPC import *
import server
import random

from game_world import remove_obj
from stage1 import Block, Arrow, Ladder, Box, Door
from stage2 import Block, Ladder, Box


center_x = screen_width/2
center_y = screen_height/2


def load_stage(stage_number):
    stage_module_name = f"stage{stage_number}"
    stage_module = importlib.import_module(stage_module_name)

    Block = getattr(stage_module, "Block")
    Ladder = getattr(stage_module, "Ladder")
    Box = getattr(stage_module, "Box")

    return Block, Ladder, Box

stage_config = {
    1: {
        "module": "stage1",
        "background": "Background1",
        "npcs": [NPC_snake, NPC_bat],
        "npc_positions": [(300, 150), (600, 250), (800, 350)]
    },
    2: {
        "module": "stage2",
        "background": "Background2",
        "npcs": [NPC_snail, NPC_mini_frog],
        "npc_positions": [(300, 150), (600, 250), (800, 350)],
    }
}


def remove_all_npcs():
    for npc in server.npcs:
        game_world.remove_obj(npc)  # 게임 월드에서 NPC 제거
    server.npcs.clear()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            #game_framework.change_mode(title_mode)
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:  # P키 입력 처리
            remove_all_npcs()  # NPC 모두 제거
        else:
            server.hero.handle_event(event)

def init(stage_number=None):
    print(f"Initializing Stage {stage_number}")
    global Running

    finish()

    stage_number = server.stage_number
    Running = True
    config = stage_config[stage_number]
    stage_module = importlib.import_module(config["module"])

    background_class_name = config["background"]
    background_module = importlib.import_module("background")
    background_class = getattr(background_module, background_class_name)
    server.background = background_class()
    game_world.add_obj(server.background, 0)

    Block, Ladder, Box = load_stage(stage_number)

    server.block = Block(world_width, 60, world_width // 2, 10, is_background=True)
    game_world.add_obj(server.block, 0)
    game_world.add_collision_pair('block:hero', server.block, None)
    game_world.add_collision_pair('block:bomb', server.block, None)


    # w, h, xPos, yPos
    block_positions = [(100, 50, 1000, 200), (100, 50, 300, 200), (100, 50, 650, 300)]
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

    ladder_positions = [(900, 110), (200, 110), (550, 210)]
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
    init_npcs(stage_number)

def init_npcs(stage_number):
    print(f'{stage_number}')
    config = stage_config[stage_number]

    npcs = config["npcs"]  # 현재 스테이지에서 등장할 NPC 클래스 리스트
    npc_positions = config["npc_positions"]  # NPC 위치 리스트

    server.npcs = []
    for i, pos in enumerate(npc_positions):
        npc_class = npcs[i % len(npcs)]  # NPC 종류 순환
        npc = npc_class(*pos)  # NPC 생성
        server.npcs.append(npc)
        game_world.add_obj(npc, 0)  # 게임 월드에 추가

        # 충돌 그룹 등록
        game_world.add_collision_pair(f'hero:npc_{npc_class.__name__.lower()}', server.hero, npc)
        game_world.add_collision_pair(f'whip:npc_{npc_class.__name__.lower()}', None, npc)

hero_state = {}

def save_hero_state(hero):
    hero_state['hp'] = server.hero.hp
    hero_state['bomb_count'] = server.hero.bombCount

def load_hero_state(hero):
    server.hero.hp =  hero_state['hp']
    server.hero.bombCount = hero_state['bomb_count']

def next_stage(current_stage, hero):
    save_hero_state(hero)
    server.stage_number += 1
    print(f'{server.stage_number}')

    if server.stage_number in stage_config:
        new_stage_module = importlib.import_module(stage_config[server.stage_number]["module"])
        init(server.stage_number)
        load_hero_state(hero)  # 영웅 상태 로드
    #else:
        #game_framework.change_mode(title_mode)

def check_npc_clear(stage):
    if not server.npcs and server.door is None:
        config = stage_config[stage]
        stage_module = importlib.import_module(config["module"])
        DoorClass = getattr(stage_module, "Door")
        door = Door(400, 100)  # 문 위치 설정

        server.door = door
        game_world.add_obj(door, 0)  # 게임 월드에 문 추가
        game_world.add_collision_pair('hero:door', server.hero, door)


def finish():
    game_world.clear()
    pass

def handle_collisions():
    for group, pairs in list(game_world.collision_pairs.items()):
        for a in pairs[0]:
            for b in pairs[1]:
                if game_world.collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def update():
    game_world.update(server.hero.x, server.hero.y)
    handle_collisions()
    delay(0.01)
    check_npc_clear(server.stage_number)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass