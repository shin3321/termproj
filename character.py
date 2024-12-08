from idlelib.configdialog import font_sample_text
from turtledemo.chaos import jumpto

import game_mode
import game_world
from NPC import NPC_snake
from Weapon import Bomb, Whip
from character_move import *
from background import *
from statemachine import *
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Character:
    game_mode_sound = None
    def __init__(self):
        self.frame = 0
        self.action = 1
        self.hp = 5
        self.face_dir = 1
        self.dir = 1
        self.frame_update_time = 0
        self.jump_height = 15
        self.gravity = -0.5
        self.jump_velocity = 0.1
        self.jump_height = 7
        self.bombCount = 5
        self.velocity_x, self.velocity_y = 50, 30
        self.image = load_image('img/hero.png')#125,138
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start([Idle])
        self.x = server.background.w // 2
        self.y = 88
        self.vy = 0
        self.invincible_time = 0
        self.image_alpha = 255
        self.is_invincible = False
        self.last_time = 0
        self.sx, self.sy = get_canvas_width() // 2, get_canvas_height() // 2
        self.whip = None
        self.is_jumping = False
        self.is_moving = False
        self.on_ground = True
        self.up=0
        if not Character.game_mode_sound:
            Character.game_mode_sound=  load_wav('sound/background.wav')
            Character.game_mode_sound.set_volume(32)
        Character.game_mode_sound.repeat_play()

        self.state_machine.set_transitions(
            {
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
                       z_up: Walk,
                       isAbleLadder: Ladder
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
                Attacked: {time_out: Idle,

                },
                Ladder:{w_down: Ladder, s_down: Ladder,
                         w_up: Ladder, s_up: Ladder,
                        space_down: Jump,
                        space_up: Jump,
                        exit_ladder: Idle,
                        }
            }
        )

    def update(self):
        self.state_machine.update()
        if not self.on_ground:
            self.vy += self.gravity * game_framework.frame_time
            self.y += self.vy * game_framework.frame_time

        elif self.on_ground:
            self.vy = 0


        # if self.y < server.block.height:  # 바닥 y 좌표
        #     self.y = 60
        #     self.jump_velocity = 0
        #     self.is_jumping = False


    def handle_event(self, event):
        self.state_machine.add_event( ('INPUT', event) )


    def draw(self):
        sx = self.x - server.background.window_left

        sy = self.y - server.background.window_bottom
        self.font.draw(self.x + 50, self.y + 50, f'{self.hp:02d}, {self.bombCount:02d}', (255, 255, 0))

        draw_rectangle(*self.get_bb())

        self.state_machine.draw(self)

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 30, sy - 40, sx + 30, sy + 25

    def handle_collision(self, group, other):
        if group.startswith('hero:npc_') and not self.is_invincible:
            if self.hp >= 1:
                self.hp -= 1
                self.is_invincible = True
                self.invincible_time = 2.0
                self.image_alpha = 128
               # self.bounce_count = 5
                self.state_machine.add_event(('CHANGE', 0))
            elif self.hp < 1:
                self.hp = 5
                game_mode.reset()
                # #self.hp = 5
                # #self.bombCount = 0
                # game_mode.finish()
                # #self.state_machine.start([Idle])
                # server.stage_number = 1
                # self.state_machine.add_event(('START', 0))
                # game_mode.init(server.stage_number)


        if group == 'block:hero':
            if self.vy < 0:
                self.vy = 0
                self.jump_velocity = 0
                self.is_jumping = False
                self.on_ground = True
                self.y = other.yPos + other.height // 2 + 46 # 캐릭터를 블록 위로 이동
            else:
                self.on_ground = False
        else:
            #print(f'{self.on_ground}')
            if not group.startswith('ladder:') and group.startswith('block:'):
                self.on_ground = False


        if group == 'ladder:hero':
            if abs(self.x - other.x) < 1.0:
                self.vy = 0
                self.velocity_y = 0
                self.x = other.x
                self.state_machine.add_event(('ladder', 0))

        else:
            self.on_ground = True
            self.state_machine.add_event(('exit_ladder', 0))

    # def bounce_back(self):
    #     if self.bounce_count > 0:
    #         closest_block = None
    #         min_distance = float('inf')
    #         self.x -= self.velocity_x
    #
    #         for block in server.block:
    #             if self.y >= block.yPos + block.height // 2 + 10:
    #                 distance = abs(self.x - block.xPos)
    #                 if distance < min_distance:
    #                     min_distance = distance
    #                     closest_block = block
    #
    #         if closest_block:
    #             self.x -= self.velocity_x
    #             self.y = closest_block.yPos + closest_block.height // 2 + 40
    #             self.velocity_y = max(self.velocity_y, 0)
    #             self.velocity_y += self.gravity
    #             self.bounce_count -= 1


    def bomb(self, vel):
        if self.bombCount > 0:
            bomb = Bomb(self.x, self.y, self.face_dir * vel)
            game_world.add_obj(bomb, 1)
            game_world.add_collision_pair('bomb:npc_snake', bomb, None)

            game_world.add_collision_pair('block:bomb', None, bomb)
            game_world.add_collision_pair('bomb:box', bomb, None)
            for npc in server.npcs:
                #print(f'{npc}')
                game_world.add_collision_pair('bomb:npc_', bomb, npc)

            self.bombCount -= 1
        elif self.bombCount == 0:
            pass

    def create_whip(self):
        self.whip = Whip(self.x, self.y, self.face_dir) #12, 3, 6
        game_world.add_obj(self.whip, 0)

        game_world.add_collision_pair('box:whip', None, self.whip)

        for npc in server.npcs:
            npc_class_name = npc.__class__.__name__.lower()
            print(f'Adding collision for {npc_class_name}')
            game_world.add_collision_pair(f'whip:npc_{npc_class_name}', self.whip, npc)






