from turtledemo.forest import symRandom

from pico2d import *
from statemachine import *
from map import *

center_x = screen_width/2
center_y = screen_height/2

class Idle:
    @staticmethod
    def enter(hero, e):
        if a_up(e) or d_down(e) or start_event(e):
            hero.face_dir = -1

        elif d_up(e) or a_down(e):
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
            hero.image.clip_draw(0,1910, 125, 138, hero.x, hero.y, 100, 100)
        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(0, 1910, 125, 138, 0, 'h', hero.x, hero.y, 100, 100)


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
            hero.image.clip_draw(125 * hero.frame,1910,
                             125, 138, hero.x, hero.y, 100, 100)

        if hero.dir == -1:
            hero.image.clip_composite_draw(125 * hero.frame,1910,
                             125, 138, 0,'h', hero.x, hero.y, 100, 100)

class Run:
    pass

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
        hero.image.clip_draw(1130, 1910,
                             125, 138, hero.x, hero.y, 100, 100)


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
            hero.image.clip_draw(250, 1775,
                             145, 130, hero.x, hero.y-5, 100, 100)
        elif hero.face_dir == -1:
            hero.image.clip_composite_draw(250, 1775,
                                 145, 130, 0, 'h', hero.x, hero.y-5, 100, 100)