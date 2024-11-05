import character
from NPC import NPC_bat
from character import Character

world = [[], []]

def add_obj(o, depth):
    world[depth].append(o)


def update(player_x, player_y):
    for layer in world:
        for o in layer:
            if isinstance(o, NPC_bat):
                o.update(player_x, player_y)
            else:
                o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_obj(o):
    print(f'     객체 {o}를 지우려고 합니다.')
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
        print(f'     CRITICAL: 존재하지 않은 객체{o}를 지우려고 합니다.')


