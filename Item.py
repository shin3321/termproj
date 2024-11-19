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
        self.frmaeY = random.randint(0, 15)


    def update(self):
        pass


    def draw(self):
        pass


    def get_bb(self):
        return self.x - 25, self.y -25, self.x + 25, self.y+25

    def handle_collision(self, group, other):
        pass
