from idlelib.debugger_r import frametable

from pico2d import *
from sdl2.examples.gfxdrawing import draw_circles

import game_world
import server

img_size = 128


class Whip:
    whip_sound = None
    def __init__(self, x, y, face_dir):
        self.image = load_image('img/hero.png') #12, 3, 6
        self.x, self.y = x, y-23
        self.frame = 11
        self.start_time = get_time()
        self.frame_update_time = 0
        self.face_dir = face_dir

        if not Whip.whip_sound:
            Whip.whip_sound = load_wav('sound/whip.wav')
            Whip.whip_sound.set_volume(32)

    def update(self):
        current_time = get_time()
        if current_time - self.frame_update_time >= 0.40:
            self.frame_update_time = current_time
            if self.frame < 16:
                self.frame += 1

            else:
                self.frame = 10


        if get_time() - self.start_time > 1.1:
            Whip.whip_sound.play()
            server.hero.whip = None
            game_world.remove_obj(self)



    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.frame >= 10 and self.frame <= 13 and self.face_dir == 1:
            self.image.clip_draw(img_size * self.frame, img_size * 3,
                             img_size, img_size, self.x-5, self.y, 70, 70)
        elif self.frame >= 14 and self.face_dir == 1:
            self.image.clip_draw(img_size * self.frame, img_size * 3,
                                 img_size, img_size, self.x+46, self.y, 70, 70)

        if self.frame >= 10 and self.frame <= 13 and self.face_dir == -1:
            self.image.clip_composite_draw(img_size * self.frame, img_size * 3,
                             img_size, img_size,  0, 'h', self.x+10, self.y, 70, 70)
        elif self.frame >= 14 and self.face_dir == -1:
            self.image.clip_composite_draw(img_size * self.frame, img_size * 3,
                                 img_size, img_size, 0, 'h', self.x-35, self.y, 70, 70)


    def clear(self):
        if self in game_world.world:
            game_world.remove_obj(self)
        pass

    def get_bb(self):
        if self.frame >= 10 and self.frame <= 13 and self.face_dir == 1 :
            return self.x, self.y , self.x, self.y
        if self.frame >=14 and self.face_dir == 1:
            return self.x - 20, self.y - 20, self.x+70, self.y+20
        if self.frame >= 10 and self.frame <= 13 and self.face_dir == -1 :
            return self.x, self.y , self.x, self.y
        if self.frame >=14and self.face_dir == -1:
            return self.x - 70, self.y - 20, self.x-20, self.y+20
        pass

    def handle_collision(self, group, other):
        # if group.startswith('whip:npc_'):
        #     #print('Whip attack')
        #     if other in game_world.world[0]:
        #         game_world.remove_obj(other)
        pass




class Bomb: #(1, 6)
    image = None
    gravity = -0.05

    def __init__(self, x, y, velocity):
        if Bomb.image == None:
            self.image = load_image('img/items.png')
        self.x, self.y = x, y
        self.velocity_x = velocity * 2
        self.velocity_y = abs(velocity)
        self.frame = 0
        self.start_time = get_time()
        self.bomb_timer_sound = load_wav('sound/bomb_timer.wav')
        self.bomb_timer_sound.set_volume(32)
        self.bomb_sound = load_wav('sound/splash.wav')
        self.bomb_sound.set_volume(32)



    def draw(self):
        draw_rectangle(self.x - 50, self.y, self.x + 50, self.y + 50)
        self.image.clip_draw(img_size*self.frame, img_size*10, img_size,img_size,self.x, self.y, 50, 50)


    def get_bb(self):
            return self.x - 50, self.y, self.x + 50, self.y + 50

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += Bomb.gravity
        self.bomb_timer_sound.play()
        if get_time() - self.start_time > 2 :
            self.frame = (self.frame + 2) % 3

        # 5초가 지나면 삭제
        if get_time() - self.start_time > 5:
            self.bomb_timer_sound=None
            self.bomb_sound.play()
            game_world.remove_obj(self)

        # 충돌 체크
        self.check_collision()

    def check_collision(self):
        bomb_bb = self.get_bb()
        for group, (group_a, group_b) in game_world.collision_pairs.items():
            if self in group_a:
                for obj in group_b:
                    if game_world.collide(self, obj):
                        self.handle_collision(group, obj)

    def handle_collision(self, group, other):
        if group.startswith('bomb:npc_') or  group == 'bomb:box' :
            if game_world.collide(self, other):
                game_world.schedule_remove(other, 4.5)
        if group == 'block:bomb':
            self.velocity_x, self.velocity_y = 0, 0

