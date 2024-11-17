from pico2d import *
import server
from background import world_width

img_size = 128

class Block:
    def __init__(self):
        self.x, self.y = world_width/2, 0
        self.width = get_canvas_width()
        self.height = 60
        self.image = load_image('img/1Tileset.png')

    def draw(self):
        num_copies = int(world_width / 255) + 1
        draw_rectangle( self.x - 5, self.y - 5, self.x + 5, self.y + 5)
        for i in range(num_copies):
            x_position = i * 255
            self.image.clip_draw(0, 190, 255, self.height, x_position, self.y)

        num_copies = int(world_width / 60) + 1
        for i in range(num_copies):
            x_position = i * 60
            self.image.clip_draw(320, 405, 60, 50, x_position, self.height-10)



    def update(self):
        pass


    def get_bb(self):
        num_copies_large_tile = int(world_width / 255) + 1
        num_copies_small_tile = int(world_width / 60) + 1

        total_height = self.height + 50  # 블럭의 전체 높이
        return 0, 0, world_width+50, total_height+50


class Arrow:
    def __init__(self):
        self.x, self.y = 400, 100
        self.gravity = 0.5

        self.image = load_image('img/items.png')

    def update(self):
        if server.hero.y == self.y:
            self.y -= self.gravity
            self.x += 1

        pass
    def draw(self):
        self.image.clip_draw(img_size ,img_size*14, img_size, img_size, self.x, self.y, 50, 50)
        pass

    def handle_collision(self, group, other):
        pass
