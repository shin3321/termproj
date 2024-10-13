from pico2d import *
import random
from map import *

class Character:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.hp = 100
        self.image = load_image('img/hero.png')#125,138
        pass


    def update(self):
        pass


    def move(self): #fram = 8
        '''
        key = 1, up
        key = 2, left
        key = 3, down
        key = 4, right
        key = 5, space jump
        key = 6, z attack
        key = 7, x bomb
        key = 8, s loop
        key = 9, lshift  speed up
        '''

        pass

    def attack(self):
        pass

    def draw(self):
        self.image.clip_draw(0,1910, 125, 138, self.x, self.y, 100, 100)


character = Character(screen_width/2, screen_height/2)

