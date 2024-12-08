from random import randint

from pico2d import *
import random
import importlib

import finale
import game_framework
import game_world
import title_mode
from character import Character
from background import *
from NPC import *
import server
import random

from character_move import Idle
from game_world import remove_obj
from stage1 import Block, Ladder, Box
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
        "npc_positions": [(300, 250), (600, 250), (750, 350)]
    },
    2: {
        "module": "stage2",
        "background": "Background2",
        "npcs": [NPC_snail, NPC_mini_frog],
        "npc_positions":  [(300, 250), (850, 350), (600, 350)],
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
            game_framework.change_mode(title_mode)
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


    block_positions = [
        (world_width, 60, world_width // 2, 10, True),  # is_background 추가
        (130, 50, 1050, 300, False),
        (100, 50, 300, 200, False),
        (100, 50, 650, 300, False)
    ]

    server.block = [Block(width, height, x, y, is_bg) for width, height, x, y, is_bg in block_positions]

    for block in server.block:
        game_world.add_obj(block, 0)
        game_world.add_collision_pair('block:hero', block, None)
        game_world.add_collision_pair('block:bomb', block, None)

    box_positions = [
        (1050, 350),
        (650, 350),
        (350, 250),
        (500, 65),
        (700, 65)
    ]

    server.boxs = [Box(x, y) for x, y in random.sample(box_positions, k=5)]
    for box in server.boxs:
        game_world.add_obj(box, 0)
        game_world.add_collision_pair('box:whip', box, None)
        game_world.add_collision_pair('bomb:box', None, box)

    ladder_positions = [(1050, 205), (200, 105), (550, 205)]
    server.ladders = [Ladder(x, y) for x, y in ladder_positions]
    for ladder in server.ladders:
        game_world.add_obj(ladder, 0)
        game_world.add_collision_pair('ladder:hero', ladder, None)  # 각 사다리에 대해 등록

    server.hero = Character()
    game_world.add_obj(server.hero, 1)
    game_world.add_collision_pair('block:hero', None, server.hero)
    game_world.add_collision_pair('ladder:hero', None, server.hero)
    game_world.add_collision_pair('item:hero', None, server.hero)

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

        game_world.add_collision_pair(f'hero:npc_{npc_class.__name__.lower()}', server.hero, npc)
        game_world.add_collision_pair(f'whip:npc_{npc_class.__name__.lower()}', None, npc)
        game_world.add_collision_pair(f'bomb:npc_{npc_class.__name__.lower()}', None, npc)

hero_state = {}

def save_hero_state(hero):
    hero_state['hp'] = server.hero.hp
    hero_state['bomb_count'] = server.hero.bombCount

def load_hero_state(hero):
    server.hero.hp =  hero_state['hp']
    server.hero.bombCount = hero_state['bomb_count']
    #server.hero.state_machine.start([Idle])

def next_stage(current_stage, hero):
    save_hero_state(hero)
    server.stage_number = current_stage + 1
    game_world.clear()
    server.hero = None
    server.block = None
    server.npcs = None
    server.boxs = None
    server.ladders = None
    server.door = None

    if server.stage_number in stage_config:
        new_stage_module = importlib.import_module(stage_config[server.stage_number]["module"])
        init(server.stage_number)
        load_hero_state(hero)  # 영웅 상태 로드
    else:
        game_framework.change_mode(finale)
        return

def check_npc_clear(stage):
    if not server.npcs and server.door is None:
        config = stage_config[stage]
        stage_module = importlib.import_module(config["module"])
        DoorClass = getattr(stage_module, "Door")
        print(f'{stage_module}')
        door = DoorClass(900, 140)  # 문 위치 설정

        server.door = door
        game_world.add_obj(door, 0)  # 게임 월드에 문 추가
        game_world.add_collision_pair('hero:door', server.hero, door)

def reset():
    finish()
    init(stage_number=1)
    pass

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
 #   delay(0.01)
    check_npc_clear(server.stage_number)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass