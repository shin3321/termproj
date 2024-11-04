from NPC import NPC_bat

world = [[], []]

def add_obj(o, depth):
    world[depth].append(o)


def update():
    for layer in world:
        for o in layer:
            if isinstance(o, NPC_bat):
                o.update(player.x, player.y)  # player 위치 전달
            else:
                o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_obj(o):
    for layer in world:
        for o in layer:
            layer.remove(o)
            return
        print(f'     CRITICAL: 존재하지 않은 객체{o}를 지우려고 합니다.')


