from pico2d import *
import server
from Item import Item
from background import world_width
from game_world import remove_obj, add_obj

img_size = 128

class Block:
    def __init__(self):
        self.x, self.y = world_width/2, 0
        self.width = get_canvas_width()
        self.height = 60
        self.yPos = 30
        self.image = load_image('img/1Tileset.png')

    def draw(self):
        draw_rectangle(0, 0, world_width + 50, self.height-15)
        num_copies = int(world_width / 255) + 1
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

        return 0, 0, world_width + 50, self.height-15

    def handle_collision(self, group, other):
        pass

class Block1:
    def __init__(self, w, h, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.width = w
        self.height = h
        self.image = load_image('img/1Tileset.png')


    def update(self):
        pass


    def draw(self):
        #num_copies = int( self.width / 255) + 1
        #for i in range(num_copie
            #x_position = i * 60
        draw_rectangle(self.xPos - (self.width+20) , self.yPos - (self.height / 2), self.xPos + (self.width+20),
                           self.yPos + (self.height / 2))

        self.image.clip_draw(0, 190, 255, self.height, self.xPos, self.yPos)
            #self.image.clip_draw(0, 190, 255, self.height, self.xPos, self.yPos)
        pass


    def get_bb(self):
        return (self.xPos - (self.width+20) , self.yPos - (self.height / 2), self.xPos + (self.width+20),
                           self.yPos)


    def handle_collision(self, group, other):
        pass


class Thorn:
    def __init__(self, w, h, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.width = w
        self.height = h
        self.image = load_image('img/1Tileset.png')

    def update(self):
        pass


    def draw(self):
        pass


    def get_bb(self):
        return 0, 0,  self.xPos + 50,  self.yPos+50

    def handle_collision(self, group, other):
        pass



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

class Ladder: # 64, 64
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 64
        self.frame = 7
        self.image = load_image('img/1Tileset.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(self.x - 30, self.y - 40, self.x+30, self.y +115)
        self.image.clip_draw(self.size * 3, self.size * 7, self.size, self.size,
                                self.x, self.y+75, 75, 75)
        self.image.clip_draw(self.size * 2, self.size * 7, self.size, self.size,
                                self.x, self.y, 75, 75)
        pass

    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        return (self.x - 30, self.y - 40, self.x+30, self.y +115)
        pass

class Box:
    def __init__(self, x, y):
        self.image = load_image('img/items.png')
        self.x, self.y = 400, 60
        self.size = 64
        self.item = None
        pass

    def update(self):
        pass

    def draw(self):
        draw_rectangle(self.x - 30, self.y - 30, self.x+30, self.y +30)
        self.image.clip_draw(img_size * 2, img_size * 15, img_size, img_size,
                                self.x, self.y, 65, 65)

        pass

    def handle_collision(self, group, other):
        if group == 'box:whip':
            print(f'{group}')
            self.item = Item(self.x, self.y)
            remove_obj(self)
            add_obj(self.item, 0)
            pass
        pass

    def get_bb(self):
        return (self.x - 30, self.y - 30, self.x+30, self.y +30)
        pass