from pico2d import *
import random

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

class NPC_bat:
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

class NPC_snail:
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


class NPC_mini_frog:
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
