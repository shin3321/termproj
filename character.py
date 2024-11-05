import game_world
from Weapon import Bomb
from character_move import *
from map import *
from statemachine import *

center_x = screen_width/2
center_y = screen_height/2

class Character:
    def __init__(self, x, y):
        self.x, self.y = x, y
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
                       s_down: Sit, x_down: Idle
                       },
                Walk: {d_down : Idle, d_up : Idle, a_down : Idle, a_up : Idle,
                       s_down: Sit, s_up: Sit,
                       lshift_down: Run,
                       x_down: Walk
                       },
                Run: {lshift_up: Walk,
                      x_down: Run
                        },
                Sit: {s_up: Idle, x_down: Sit},
                Attack: {z_down: Attack}
                #WalkAttack: {time_out: Walk},
               # RunAttack: {time_out: Run}

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

    def bomb(self, vel):
        bomb = Bomb(self.x, self.y, self.face_dir * vel)
        game_world.add_obj(bomb, 1)



class Whip:
    def __init__(self):
        self.image = load_image('img/hero.png')
