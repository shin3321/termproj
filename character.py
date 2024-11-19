from idlelib.configdialog import font_sample_text

import game_mode
import game_world
from NPC import NPC_snake
from Weapon import Bomb, Whip
from character_move import *
from background import *
from statemachine import *
import server

class Character:
    def __init__(self):
        self.frame = 0
        self.action = 1
        self.hp = 1000
        self.face_dir = 1
        self.dir = 1
        self.frame_update_time = 0
        self.jump_velocity = 50
        self.jump_height = 20
        self.gravity = -1
        self.velocity_x, self.velocity_y = 30, 30
        self.image = load_image('img/hero.png')#125,138
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start([Idle])
        self.x = server.background.w // 2
        self.y = server.block.height +50
        self.vy = 0 #중력 받게 해서 항상 블록 위에 서 있게 하기
        self.invincible_time = 0
        self.image_alpha = 255
        self.is_invincible = False
        self.last_time = 0
        self.sx, self.sy = get_canvas_width() // 2, get_canvas_height() // 2
        self.whip = None
        self.is_jumping = False
        self.is_moving = False
        self.on_ground = False
        self.state_machine.set_transitions(
            {
                Sleep: {space_down : Idle,
                        d_down : Walk, d_up : Walk,
                        s_down: Sit
                        },
                Idle: {
                       d_down : Walk,  a_down : Walk, a_up : Walk, d_up : Walk,
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
                       changeHp: Attacked,
                       space_up: Walk,
                       z_up: Walk
                       },
                # Run: {lshift_up: Walk,
                #       x_down: Run
                #         },
                Sit: {s_up: Idle, x_down: Sit},
                Attack: {z_down: Attack,
                         time_out: Idle,
                         d_down: Walk,  a_down: Walk,
                         changeHp: Attacked,
                         },
                Jump: {s_down: Sit, x_down: Jump,
                       z_down: Attack,
                       space_down: Jump,
                       changeHp: Attacked,
                       d_down: Walk, a_down: Walk,
                       d_up: Idle, a_up: Idle,
                       walk: Walk, idle: Idle
                        },
                Attacked: {time_out: Idle
                }


            }
        )


    def update(self):
        if self.on_ground == False:
            self.velocity_y = 30
            self.vy += self.gravity
            self.y += self.vy * game_framework.frame_time

        elif self.on_ground == True:
            self.velocity_y = 0
            self.state_machine.update()

        # if self.y < server.block.height:  # 바닥 y 좌표
        #     self.y = 60
        #     self.jump_velocity = 0
        #     self.is_jumping = False


    def handle_event(self, event):
        self.state_machine.add_event( ('INPUT', event) )


    def draw(self):
        self.font.draw(self.x + 50, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        draw_rectangle(self.x - 30, self.y - 40, self.x + 30, self.y + 30)
        self.sx, self.sy = get_canvas_width() // 2, get_canvas_height() // 2
        self.state_machine.draw(self)

    def get_bb(self):
        # fill here
        return self.x - 30, self.y - 40, self.x + 30, self.y + 30
        pass

    def handle_collision(self, group, other):
        if group == 'hero:npc_snake' and not self.is_invincible:
            if self.hp > 1:
                self.hp -= 1
                self.is_invincible = True
                self.invincible_time = 2.0
                self.image_alpha = 128
                self.bounce_count = 5
                self.state_machine.add_event(('CHANGE', 0))
            # elif self.hp < 1:
            #     self.hp = 5
            #     #초기 상태로
            #     pass
        if group == 'block:hero':
            self.is_jumping = False
            self.on_ground = True

        if group == 'block1:hero':
            print(f'{group}')
            self.is_jumping = False
            self.on_ground = True
            self.y = other.yPos + other.height

        if group == 'ladder:hero':
            self.state_machine.add_event(('ladder', 0))

            pass

    def bounce_back(self):
        if self.bounce_count > 0:
            self.x -= self.velocity_x
            self.velocity_y += self.gravity * self.velocity_y
            self.y += self.velocity_y
            self.bounce_count -= 1

    def bomb(self, vel):
        bomb = Bomb(self.x, self.y, self.face_dir * vel)
        game_world.add_obj(bomb, 1)
        game_world.add_collision_pair('bomb:npc_snake', bomb, None)
        game_world.add_collision_pair('block:bomb', None, bomb)

    def create_whip(self):
        self.whip = Whip(self.x, self.y, self.face_dir) #12, 3, 6
        game_world.add_obj(self.whip, 0)

        for npc_snake in game_world.world[0]:
            if isinstance(npc_snake, NPC_snake):
                game_world.add_collision_pair('whip:npc_snake', self.whip, npc_snake)




