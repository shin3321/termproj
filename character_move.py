from turtledemo.forest import symRandom

from pico2d import *

import game_framework
from statemachine import *
from background import *

PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
RUN_SPEED_KMPH = 20  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

img_size = 128

class Idle:
    @staticmethod
    def enter(hero, e):
        if a_up(e) or d_down(e) :
            hero.face_dir = -1

        elif d_up(e) or a_down(e) or start_event(e):
            hero.face_dir = 1

        hero.action = 1
        hero.frame = 0
        hero.is_moving = False

        hero.start_time = get_time()
        pass

    @staticmethod
    def exit(hero, e):
        if x_down(e):
            hero.bomb(3)
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1) % 1
        if get_time() - hero.start_time > 60:
            # 이벤트 발생
            hero.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(0, img_size*15,
                                 img_size, img_size, hero.x, hero.y, 100, 100)

        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(0, img_size*15,
                                           img_size, img_size, 0, 'h', hero.x, hero.y, 100, 100)

class Walk:
    @staticmethod
    def enter(hero, e):
        if d_down(e) or a_up(e):
            hero.dir = 1

        if a_down(e) or d_up(e):
            hero.dir = -1

        hero.action = 1
        hero.is_moving = True

    @staticmethod
    def exit(hero, e):
        if x_down(e):
            hero.bomb(3.5)
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1) % 9
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.image.clip_draw(img_size * hero.frame,img_size*15,
                             img_size, img_size, hero.x, hero.y, 100, 100)

        if hero.dir == -1:
            hero.image.clip_composite_draw(img_size * hero.frame,img_size*15,
                             img_size, img_size, 0,'h', hero.x, hero.y, 100, 100)

class Jump:
    @staticmethod
    def enter(hero, e):
        hero.jump_velocity = 10
        hero.is_jumping = True
        if space_down(e):
            pass
        if d_down(e):
            hero.dir = 1
        if a_down(e):
            hero.dir = -1


    @staticmethod
    def exit(hero, e):
        if x_down(e):
            hero.bomb(3.5)
        hero.is_jumping = False

        pass
    @staticmethod
    def do(hero):
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        hero.y += hero.jump_velocity
        hero.jump_velocity += hero.gravity

        if hero.y <= server.block.height + 25:
            hero.on_ground = True
            hero.jump_velocity = 0
            if hero.is_moving != False:  # 이동 중이면 Walk 상태
                hero.state_machine.add_event(('WALK', 0))
            else:  # 정지 상태면 Idle 상태
                hero.state_machine.add_event(('IDLE', 0))

    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.image.clip_draw(img_size * hero.frame,img_size*15,
                             img_size, img_size, hero.x, hero.y, 100, 100)

        if hero.dir == -1:
            hero.image.clip_composite_draw(img_size * hero.frame,img_size*15,
                             img_size, img_size, 0,'h', hero.x, hero.y, 100, 100)


class Sleep:
    @staticmethod
    def enter(hero, e):
        pass
    @staticmethod
    def exit(hero, e):
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1)
    @staticmethod
    def draw(hero):
        hero.image.clip_draw(1130, img_size*15,
                             img_size, img_size, hero.x, hero.y, 100, 100)


class Sit:
    @staticmethod
    def enter(hero, e):
         hero.action = 2
         hero.is_moving = False

    @staticmethod
    def exit(hero, e):
        if x_down(e):
            hero.bomb(0.2)
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1)%1

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(img_size*2, img_size*14,
                             img_size, img_size, hero.x, hero.y-5, 100, 100)
        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(250, img_size*14,
                                 img_size, img_size, 0, 'h', hero.x, hero.y-5, 100, 100)

class Attack:   #(4, 5, 8frame)
    @staticmethod
    def enter(hero, e):
        hero.frame_update_time = 0
        hero.start_time = get_time()
        hero.create_whip()
        hero.frame = 4
        if z_down(e) and a_down(e):
            hero.dir = -1

        if z_down(e) and d_down(e):
            hero.dir = 1
            pass

    @staticmethod
    def exit(hero, e):
        hero.whip.clear()
        pass

    @staticmethod
    def do(hero):
        current_time = pico2d.get_time()
        if current_time - hero.frame_update_time >= 0.1:  # 속도를 조절하려면 0.1초 조정

            hero.frame = (hero.frame + 1) % 7
            hero.frame_update_time = current_time

        if get_time() - hero.start_time > 1.2:
            hero.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(img_size * hero.frame, img_size * 11,
                                 img_size, img_size, hero.x, hero.y, 100, 100)

        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(img_size * hero.frame, img_size * 11,
                                           img_size, img_size, 0, 'h', hero.x, hero.y - 5, 100, 100)

class Attacked:
    @staticmethod
    def enter(hero, e):
        hero.frame = 0
        hero.start_time = get_time()
        hero.is_moving = False
        pass

    @staticmethod
    def exit(hero, e):

        pass

    @staticmethod
    def do(hero):
        current_time = get_time()
        if current_time - hero.frame_update_time >= 0.10:
            hero.frame_update_time = current_time
            hero.frame = hero.frame % 4 +1

            if get_time() - hero.start_time > 1.2:
                hero.frame = 4

        if hero.is_invincible:
            hero.image_alpha = 128 if int(get_time() * 10) % 2 == 0 else 255
            hero.bounce_back()

        hero.invincible_time -= pico2d.get_time() - hero.last_time
        if hero.invincible_time <= 0:
            hero.is_invincible = False
            hero.image_alpha = 255
            hero.state_machine.add_event(('TIME_OUT', 0))

        hero.last_time = pico2d.get_time()

    @staticmethod
    def draw(hero):
        hero.image.opacify(hero.image_alpha / 255.0)
        if hero.frame < 4:
            hero.image.clip_draw(img_size * hero.frame, img_size * 14,
                                 img_size, img_size, hero.x, hero.y, 100, 100)
        elif hero.frame == 4:
            hero.frame = 9
            hero.image.clip_draw(img_size * hero.frame, img_size * 15,
                                 img_size, img_size, hero.x, hero.y, 100, 100)
        hero.image.opacify(1.0)
