import random

from pico2d import *

from game_world import remove_obj

img_size = 128

class Item:
    def __init__(self, x, y):
        self.image = load_image('img/Items.png')
        self.size = 50
        self.x = x
        self.y = y
        self.frameX = random.randint(0, 1)
        self.frameY = 13 #random.randint(14, 15)


    def update(self):
        pass


    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(img_size * self.frameX, img_size * self.frameY,
                             img_size, img_size, self.x, self.y, 65,65 )
        pass


    def get_bb(self):
        return self.x - 25, self.y -25, self.x + 25, self.y+25

    def handle_collision(self, group, other):
        if group == 'item:hero':
            print(f'{group}')
            if self.frameX == 0:
                other.bombCount += 1
            elif self.frameX == 1:
                other.bombCount += 5
            remove_obj(self)
        pass
