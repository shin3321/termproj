import random

from pico2d import *

img_size = 128

class Item:
    def __init__(self, x, y):
        self.image = load_image('img/Items.png')
        self.size = 50
        self.x = x
        self.y = y
        self.frameX = random.randint(0, 15)
        self.frameY = random.randint(0, 15)


    def update(self):
        pass


    def draw(self):
        self.image.clip_draw(img_size * self.frameX, img_size * self.frameY,
                             img_size, img_size, self.x, self.y, 65,65 )
        pass


    def get_bb(self):
        return self.x - 25, self.y -25, self.x + 25, self.y+25

    def handle_collision(self, group, other):
        pass
