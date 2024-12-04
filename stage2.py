from pico2d import  *

import game_mode
import game_world
import server
from Item import Item
from background import world_width

img_size = 128

class Block:
    def __init__(self, width, height, xPos, yPos, is_background=False):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.is_background = is_background
        self.image = load_image('img/Jungle_Tiles.png')

    def draw(self):
        draw_rectangle(*self.get_bb())

        if self.is_background:  # 배경 블록 처리
            num_copies = int(world_width / 255) + 1
            for i in range(num_copies):
                x_position = i * 255
                self.image.clip_draw(0, img_size*5, 255, self.height, x_position, self.yPos)

            num_copies = int(world_width / 60) + 1
            for i in range(num_copies):
                x_position = i * 60
                self.image.clip_draw(img_size*5, img_size*5, 60, 50, x_position, self.height - 10)
        else:
            self.image.clip_draw(0, img_size*9, 255, self.height, self.xPos, self.yPos)

    def update(self):
        pass

    def get_bb(self):
        if self.is_background:
            return 0, 0, world_width + 50, self.height - 15
        else:
            return (self.xPos - self.width,
                    self.yPos,
                    self.xPos + self.width,
                    self.yPos)

    def handle_collision(self, group, other):
        pass

class Ladder: # 64, 64
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 64
        self.frame = 7
        self.image = load_image('img/Jungle_Tiles.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(img_size * 4, img_size* 11 ,img_size, img_size,
                                self.x, self.y+75, 75, 75)
        self.image.clip_draw(img_size* 4, self.size * 18, img_size, img_size,
                                self.x, self.y, 75, 75)
        pass

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        return (self.x - 30, self.y - 40, self.x+30, self.y +115)
        pass

class Box:
    def __init__(self, x, y):
        self.image = load_image('img/items.png')
        self.x, self.y = x, y
        self.size = 64
        self.item = None
        pass

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(img_size * 2, img_size * 15, img_size, img_size,
                                self.x, self.y, 65, 65)

        pass

    def handle_collision(self, group, other):
        if group == 'box:whip':
            print(f'{group}')

            self.item = Item(self.x, self.y)

            game_world.remove_obj(self)
            game_world.add_obj(self.item, 0)
            game_world.add_collision_pair("item:hero", self.item, None )
            return

        pass

    def get_bb(self):
        return (self.x - 30, self.y - 30, self.x+30, self.y +30)
        pass

class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('img/Jungle_Tiles.png')  # 문 이미지 파일 경로 (이미지 추가 필요)
        self.width = self.image.w
        self.height = self.image.h

    def update(self):
        pass

    def draw(self):
        self.image.draw(0, 0, 360, 320, self.x, self.y)

    def handle_collision(self, group, other):
        if group == 'hero:door' and isinstance(other, server.hero):
            game_mode.next_stage(3, other)  # 문에 닿으면 스테이지 2로 전환 (여기서 '2'는 다음 스테이지 번호)
