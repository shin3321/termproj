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
        pass

    def draw(self):
        self.image.clip_draw(0,1910, 125, 138, self.x, self.y, 100, 100)


character = Character(screen_width/2, screen_height/2)

class NPC_snack:
    def __init__(self):
        self.x, self.y = random.randint(0, 400), random.randint(0, 400)
        self.frame = 0
        self.image = load_image('img/Snakes.png') #85,85
        self.hp = 50


    def update(self):
        self.frame = (self.frame + 1) % 11
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 77, 263, 77, 77, self.x, self.y, 80, 80)
        pass
