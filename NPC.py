from pico2d import *
import random

import game_framework
import game_world
import server
from server import hero
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11

animaion_names = ['Fly', 'Follow', 'Idle']

class NPC_snake:
    def __init__(self, x = 400, y = 60 ):
        self.x, self.y = x, y
        self.i_x = 79
        self.i_y = 87
        self.frame = 0
        self.speed = 0.5
        self.move_x = 1
        self.action = 3
        self.image = load_image('img/Snakes.png') #85,85
        self.hp = 50
        self.dir = 1
        self.range = 25
        self.min_x = self.x - self.range  # 최소 x 좌표
        self.max_x = self.x + self.range  # 최대 x 좌표

    def update(self):

        self.frame = (
                (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11)

        # x 좌표 자동 이동
        self.x += self.speed * self.dir

        # 경계 확인 및 방향 전환
        if self.x <= self.min_x:  # 최소 경계
            self.x = self.min_x
            self.dir = 1  # 오른쪽으로 방향 전환
        elif self.x >= self.max_x:  # 최대 경계
            self.x = self.max_x
            self.dir = -1

        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * self.i_x , self.action * self.i_y ,
                                 self.i_x , self.i_y , self.x, self.y, 80, 80)
        elif self.dir == -1:
            self.image.clip_composite_draw(int(self.frame) * self.i_x, self.action * self.i_y,
                                 self.i_x, self.i_y, 0, 'h', self.x, self.y, 80, 80)
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        pass

    def handle_collision(self, group, other):
        # if group == 'hero:snake':
        #     other.hp -= 1
        #     other.is_invincible = True
        #     other.invincible_time = 2.0
        #     other.image_alpha = 128
        #     other.bounce_count = 3
        #     other.state_machine.add_event(('CHANGE', 0))
        if group == 'whip:npc_snake':
            if self in game_world.world[0]:
                game_world.remove_obj(self)

        pass

class NPC_bat:
    def __init__(self, x, y):
        self.x, self.y = random.randint(0, 800), random.randint(200, 600)
        self.frame = 1
        self.image = load_image('img/bat.png') #85,85
        self.hp = 50
        self.speed =2  # 박쥐 이동 속도
        self.state = 'Idle'
        self.build_behavior_tree()
        self.tx, self.ty = 0, 0
        self.isFollow = False

    def update(self,player_x, player_y):
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        # distance = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)
        #
        # # 특정 거리 이내로 가까워지면 쫓아가기
        # if distance < 250:  # 200 거리 내에 들어오면 쫓아오기 시작
        #
        #     self.frame = (
        #             (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3)
        #
        #     # x, y 방향의 이동량 계산
        #     direction_x = (player_x - self.x) / distance
        #     direction_y = (player_y - self.y) / distance
        #
        #     # 박쥐 위치 갱신
        #     self.x += direction_x * self.speed
        #     self.y += direction_y * self.speed
        # else:
        #     self.frame = (self.frame + 1) % 1


    def get_bb(self):
        # fill here
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(int(self.frame) * 15, 0, 15, 15, self.x, self.y, 55, 55)
        pass

    def handle_collision(self, group, other):
        if group == 'whip:npc_snake':
            if self in game_world.world[0]:
                game_world.remove_obj(self)
        pass


    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2
        pass

    def is_player_nearby(self, r):
        if self.distance_less_than(server.hero.x, server.hero.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_slightly_to(self, tx, ty):
        direction_x = tx - self.x
        direction_y = ty - self.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # 너무 가까우면 이동 완료
        if distance < 1.0:
            self.x = tx
            self.y = ty
            return BehaviorTree.SUCCESS

        # 일정 속도로 이동
        direction_x /= distance
        direction_y /= distance
        self.x += direction_x * self.speed
        self.y += direction_y * self.speed
        return BehaviorTree.RUNNING

    def move_to_player(self, r = 0.5):
        self.state = 'Fly'
        self.move_slightly_to(server.hero.x, server.hero.y)
        if self.distance_less_than(server.hero.x, server.hero.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def find_closest_block(self):
        closest_block = None
        min_distance = float('inf')

        block_center_x = server.block.xPos + (server.block.width / 2)
        block_center_y = server.block.yPos + (server.block.height / 2)

        distance = math.sqrt((self.x - block_center_x) ** 2 + (self.y - block_center_y) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_block = server.block

        return closest_block

    def sit_on_block(self):
        block = self.find_closest_block()
        if block:
            # 블록 중심 좌표로 이동
            self.tx = self.x
            self.ty = block.yPos + (block.height / 2)

            result = self.move_slightly_to(self.tx, self.ty)
            if result == BehaviorTree.SUCCESS:
                self.state = 'Sit'  # 앉기 상태로 전환
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # 플레이어가 근처에 있는지 확인하는 조건
        c1 = Condition('플레이어가 근처에 있는가?', lambda: self.is_player_nearby(7))

        # 행동: 플레이어 추적
        a1 = Action('플레이어 추적', self.move_to_player)
        chase_player = Sequence('플레이어 추적', c1, a1)

        # 행동: 블록 위 앉기
        a2 = Action('블록 위 앉기', self.sit_on_block)

        # 최상위 행동 트리
        root = Selector('최상위 행동',
                        Sequence('플레이어 근처 확인', c1, chase_player),  # 플레이어가 근처에 있을 때 반응
                        a2  # 플레이어가 멀리 있을 때 블록 위 앉기
                        )
        self.bt = BehaviorTree(root)


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
