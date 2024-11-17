import game_world
from Weapon import Bomb, Whip
from character_move import *
from background import *
from statemachine import *
import server

class Character:
    def __init__(self):
        self.frame = 0
        self.action = 1
        self.hp = 5
        self.face_dir = 1
        self.dir = 1
        self.frame_update_time = 0
        self.jump_velocity = 10
        self.jump_height = 10
        self.gravity = -1
        self.velocity_x, self.velocity_y = 30, 30
        self.image = load_image('img/hero.png')#125,138
        self.state_machine = StateMachine(self)
        self.state_machine.start([Idle])
        self.x = server.background.w // 2
        self.y = server.background.h // 2
        self.invincible_time = 0
        self.image_alpha = 255
        self.is_invincible = False
        self.last_time = 0
        self.sx, self.sy = get_canvas_width() // 2, get_canvas_height() // 2
        self.whip = None
        self.state_machine.set_transitions(
            {
                Sleep: {space_down : Idle,
                        d_down : Walk, d_up : Walk,
                        s_down: Sit
                        },
                Idle: {time_out : Sleep,
                       d_down : Walk, d_up : Walk, a_down : Walk, a_up : Walk,
                       s_down: Sit, x_down: Idle,
                       z_down: Attack,
                       space_down: Jump,
                       changeHp: Attacked
                       },
                Walk: {d_down : Idle, d_up : Idle, a_down : Idle, a_up : Idle,
                       s_down: Sit, s_up: Sit,
                       # lshift_down: Run,
                       x_down: Walk,
                       z_down: Attack,
                       space_down: Jump,
                       changeHp: Attacked
                       },
                # Run: {lshift_up: Walk,
                #       x_down: Run
                #         },
                Sit: {s_up: Idle, x_down: Sit},
                Attack: {z_down: Attack,
                         time_out: Idle,
                         d_down: Walk, d_up: Walk, a_down: Walk, a_up: Walk,
                         changeHp: Attacked
                         },
                Jump: { d_down : Walk, d_up : Walk, a_down : Walk, a_up : Walk,
                       s_down: Sit, x_down: Jump,
                       z_down: Attack,
                        space_down: Jump,
                        changeHp: Attacked},
                Attacked: {time_out: Idle
                }


            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )


    def draw(self):
        draw_rectangle(self.x-64,self.y-64,self.x+64,self.y+64)
        self.sx, self.sy = get_canvas_width() // 2, get_canvas_height() // 2
        self.state_machine.draw(self)

    def get_bb(self):
        # fill here
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50
        pass

    def handle_collision(self, group, other):
        if group == 'hero:npc_snake' and not self.is_invincible:
            self.hp -= 1
            self.is_invincible = True
            self.invincible_time = 5.0
            self.image_alpha = 128
            self.bounce_count = 3
            self.state_machine.add_event(('CHANGE', 0))
        pass

    def bounce_back(self):
        if self.bounce_count > 0:
            self.x -= self.velocity_x
            self.y += self.velocity_y
            self.velocity_y += self.gravity * self.velocity_y
            self.bounce_count -= 1

    def bomb(self, vel):
        bomb = Bomb(self.x, self.y, self.face_dir * vel)
        game_world.add_obj(bomb, 1)

    def create_whip(self):
        self.whip = Whip(self.x, self.y, self.face_dir) #12, 3, 6
        game_world.add_obj(self.whip, 0)



