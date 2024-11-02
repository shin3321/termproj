from turtledemo.forest import symRandom

from pico2d import *
from statemachine import *
from map import *

img_size = 128

class Idle:
    @staticmethod
    def enter(hero, e):
        if a_up(e) or d_down(e):
            hero.face_dir = -1

        elif d_up(e) or a_down(e)or start_event(e):
            hero.face_dir = 1

        hero.action = 1
        hero.frame = 0

        hero.start_time = get_time()
        pass
    @staticmethod
    def exit(hero, e):
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1) % 1
        if get_time() - hero.start_time > 5:
            # 이벤트 발생
            hero.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(0, img_size*15, img_size, img_size, hero.x, hero.y, 100, 100)

        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(0, img_size*15, img_size, img_size, 0, 'h', hero.x, hero.y, 100, 100)

class Walk:
    @staticmethod
    def enter(hero, e):
        if d_down(e) or a_up(e):
            hero.dir = 1

        if a_down(e) or d_up(e):
            hero.dir = -1

        hero.action = 1

    @staticmethod
    def exit(hero, e):
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1) % 9
        hero.x += hero.dir * 5
    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.image.clip_draw(img_size * hero.frame,img_size*15,
                             img_size, img_size, hero.x, hero.y, 100, 100)

        if hero.dir == -1:
            hero.image.clip_composite_draw(img_size * hero.frame,img_size*15,
                             img_size, img_size, 0,'h', hero.x, hero.y, 100, 100)

class Run:
    @staticmethod
    def enter(hero, e):
        if (d_down(e) or a_up(e)) and lshift_down(e):
            hero.dir = 1

        if (a_down(e) or d_up(e)) and lshift_down(e):
            hero.dir = -1

        hero.action = 1

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1) % 9
        hero.x += hero.dir * 15

    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.image.clip_draw(img_size * hero.frame, img_size*15,
                                 img_size, img_size, hero.x, hero.y, 100, 100)

        if hero.dir == -1:
            hero.image.clip_composite_draw(img_size * hero.frame, img_size*15,
                                           img_size, img_size, 0, 'h', hero.x, hero.y, 100, 100)


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
        if s_down(e):
            hero.action = 2
            pass

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1)

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(img_size*2, img_size*14,
                             img_size, img_size, hero.x, hero.y-5, 100, 100)
        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(250, img_size*14,
                                 img_size, img_size, 0, 'h', hero.x, hero.y-5, 100, 100)

class RunAttack:   #(4, 5, 8frame)
    @staticmethod
    def enter(hero, e):
        if z_down(e):
            hero.frame = 4
            hero.dir = 2
            hero.frame_update_time = 0
            hero.start_time = get_time()
            pass

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        current_time = pico2d.get_time()
        if current_time - hero.frame_update_time >= 0.1:  # 속도를 조절하려면 0.1초 조정
            hero.frame = (hero.frame + 1) % 8
            hero.frame_update_time = current_time
        hero.x += hero.dir*5
        if get_time() - hero.start_time > 1.5:
            hero.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(img_size * hero.frame, img_size * 11,
                                 img_size, img_size, hero.x, hero.y, 100, 100)
        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(img_size * hero.frame, img_size * 11,
                                           img_size, img_size, 0, 'h', hero.x, hero.y - 5, 100, 100)


class WalkAttack:
    @staticmethod
    def enter(hero, e):
        if z_down(e):
            hero.dir = 1
            hero.frame = 4
            hero.frame_update_time = 0
            hero.start_time = get_time()
            pass

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        current_time = pico2d.get_time()
        if current_time - hero.frame_update_time >= 0.1:
            hero.frame = (hero.frame + 1) % 8
            hero.frame_update_time = current_time
        hero.x += hero.dir * 5

        if get_time() - hero.start_time > 1.5:
            # 이벤트 발생
            hero.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        if hero.face_dir == 1:
            hero.image.clip_draw(img_size*hero.frame, img_size*11,
                                 img_size, img_size, hero.x, hero.y, 100, 100)
        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(img_size*hero.frame, img_size*11,
                                           img_size, img_size, 0, 'h', hero.x, hero.y - 5, 100, 100)
