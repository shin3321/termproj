from idlelib.debugger_r import frametable

from pico2d import *
from sdl2.examples.gfxdrawing import draw_circles

import game_world

img_size = 128

class Bomb: #(1, 6)
    image = None
    gravity = -0.1
    def __init__(self, x, y, velocity):
        if Bomb.image == None:
            self.image = load_image('img/items.png')
        self.x, self.y = x, y
        self.velocity_x = velocity * 2
        self.velocity_y = abs(velocity)
        self.frame = 0
        self.start_time = get_time()

    def draw(self):
        self.image.clip_draw(img_size*self.frame, img_size*10, img_size,img_size,self.x, self.y, 50, 50)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += Bomb.gravity

        if get_time() - self.start_time > 2:
            self.frame = (self.frame + 2) % 3

        if get_time() - self.start_time > 5 :
            game_world.remove_obj(self)





