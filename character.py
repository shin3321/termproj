from idlelib.config import IdleConf
from pico2d import *
import random
from map import *
from statemachine import StateMachine, space_down, time_out, D_down


class Idle:
    @staticmethod
    def enter(hero, e):
        pass
    @staticmethod
    def exit(hero, e):
        pass
    @staticmethod
    def do(hero):
        pass
    @staticmethod
    def draw(hero):
        hero.image.clip_draw(0,1910, 125, 138, hero.x, hero.y, 100, 100)

class RightWalk:
    @staticmethod
    def enter(hero, e):
        if D_down(e):
            hero.dir, hero.action = 1, 1
    @staticmethod
    def exit(hero, e):
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1) % 9
        hero.x += hero.dir * 5
    @staticmethod
    def draw(hero):
        hero.image.clip_draw(125 * hero.frame,1910,
                             125, 138, hero.x, hero.y, 100, 100)

class LeftWalk:
    @staticmethod
    def enter(hero, e):
        pass
    @staticmethod
    def exit(hero, e):
        pass
    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + 1)%9
    @staticmethod
    def draw(hero):
        hero.image.clip_compositie_draw(125 * hero.frame,1910,
                             125, 138, hero.x, hero.y, 100, 100)

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



class Character:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.frame = 0
        self.action = 1
        self.hp = 100
        self.image = load_image('img/hero.png')#125,138
        self.state_machine = StateMachine(self)
        self.state_machine.start(Sleep)
        self.state_machine.set_transitions(
            {
                Sleep : {space_down : Idle},
                Idle : {time_out : Sleep},
                RightWalk : {D_down : Idle, D_down : Sleep}


            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def move(self): #fr bam = 8
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
        self.state_machine.draw(self)








character = Character(screen_width/2, screen_height/2)

