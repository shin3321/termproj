from pico2d import *
import random
from map import *

class Character():
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.hp = 100
        pass

    def move(self):
        pass

character = Character(screen_width/2, screen_height/2)

class NPC():
    def __init__(self):
        self.x, self, y = random.randint(0, world_width), random.randint(0, world_height)

