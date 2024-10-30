from character_move import Idle, Walk, Sleep
from map import *
from statemachine import *


class Character:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.frame = 0
        self.action = 1
        self.hp = 100
        self.image = load_image('img/hero.png')#125,138
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Sleep: {space_down : Idle, d_down : Walk, d_up : Walk},
                Idle: {time_out : Sleep,
                       d_down : Walk, d_up : Walk, a_down : Walk, a_up : Walk},
                Walk: {d_down : Idle, d_up : Idle, a_down : Idle, a_up : Idle}


            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )



    def attack(self):
        pass

    def draw(self):
        self.state_machine.draw(self)








character = Character(screen_width/2, screen_height/2)

