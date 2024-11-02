from character_move import *
from map import *
from statemachine import *

center_x = screen_width/2
center_y = screen_height/2

class Character:
    def __init__(self, x, y):
        self.x = x
        self. y = y
        self.frame = 0
        self.action = 1
        self.hp = 100
        self.face_dir = 1
        self.dir = 1
        self.frame_update_time =0
        self.image = load_image('img/hero.png')#125,138
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Sleep: {space_down : Idle,
                        d_down : Walk, d_up : Walk,
                        s_down: Sit
                        },
                Idle: {time_out : Sleep,
                       d_down : Walk, d_up : Walk, a_down : Walk, a_up : Walk,
                       s_down: Sit
                       },
                Walk: {d_down : Idle, d_up : Idle, a_down : Idle, a_up : Idle,
                       s_down: Sit, s_up: Sit,
                       lshift_down: Run,
                       z_up: WalkAttack
                       },
                Run: {lshift_up: Walk,
                      z_up: RunAttack
                        },
                Sit: {s_up: Idle },
                WalkAttack: {time_out: Walk},
                RunAttack: {time_out: Run}

            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )


    def draw(self):
        self.state_machine.draw(self)
        draw_rectangle(self.x-64,self.y-64,self.x+64,self.y+64)

character = Character(screen_width/2, screen_height/2)

class Whip:
    def __init__(self):
        self.image = load_image('img/hero.png')