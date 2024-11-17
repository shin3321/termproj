from pico2d import *
import random

import game_world
from server import hero


class NPC_snake:
    def __init__(self, x = 400, y = 60 ):
        self.x, self.y = random.randint(0, 800), random.randint(0, 1200)
        self.i_x = 79
        self.i_y = 87
        self.frame = 0
        self.action = 3
        self.image = load_image('img/Snakes.png') #85,85
        self.hp = 50


    def update(self):
        self.frame = (self.frame + 1) % 11
        pass

    def draw(self):
        self.image.clip_draw(self.frame * self.i_x , self.action * self.i_y , self.i_x , self.i_y , self.x, self.y, 80, 80)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        # fill here
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50
        pass

    def handle_collision(self, group, other):

        pass

class NPC_bat:
    def __init__(self, x, y):
        self.x, self.y = random.randint(0, 1200), random.randint(0, 800)
        self.frame = 0
        self.image = load_image('img/bat.png') #85,85
        self.hp = 50

        self.speed =2  # 박쥐 이동 속도
        self.isFollow = False
    def update(self,player_x, player_y):
        self.frame = (self.frame + 1) % 1

        distance = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)

        # 특정 거리 이내로 가까워지면 쫓아가기
        if distance < 250:  # 200 거리 내에 들어오면 쫓아오기 시작

            self.frame = (self.frame + 1) % 3

            # x, y 방향의 이동량 계산
            direction_x = (player_x - self.x) / distance
            direction_y = (player_y - self.y) / distance

            # 박쥐 위치 갱신
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed


    def get_bb(self):
        # fill here
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 15, 0, 15, 15, self.x, self.y, 55, 55)
        pass

    def handle_collision(self, group, other):

        pass

class NPC_snail:
    def __init__(self, x = 400, y = 60):
        self.x, self.y = random.randint(0, 400), random.randint(0, 400)
        self.i_x = 80
        self.i_y = 81
        self.frame = 0
        self.image = load_image('img/snail.png') #85,85
        self.hp = 50


    def update(self):
        self.frame = (self.frame + 1) % 11
        pass

    def draw(self):
        self.image.clip_draw(self.frame * self.i_x, 0, self.i_x, self.i_y, self.x, self.y, 80, 80)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        # fill here
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50
        pass

    def handle_collision(self, group, other):

        pass

class NPC_mini_frog:
    def __init__(self, x = 400, y = 60):
        self.x, self.y = random.randint(0, 400), random.randint(0, 400)
        self.i_x = 81
        self.i_y = 70
        self.frame = 5
        self.image = load_image('img/Snakes.png') #85,85
        self.hp = 50


    def update(self):
        self.frame = (self.frame + 1) % 7

        pass

    def draw(self):
        self.image.clip_draw(self.frame * self.i_x, self.i_y, self.i_x, self.i_y, self.x, self.y, 80, 80)
        pass
