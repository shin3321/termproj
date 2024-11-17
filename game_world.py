import character
from NPC import NPC_bat
from character import Character

world = [[], []]

def add_obj(o, depth):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

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
            remove_collision_object(o)
            del o
            return
    print(f'     CRITICAL: 존재하지 않은 객체{o}를 지우려고 합니다.')

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True
    pass

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def clear():
    pass