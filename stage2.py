from pico2d import  *


class Block:
    def __init__(self):
        self.image = load_image('img/Jungle_Tiles.png')
        self.x, self.y = 0,0

    def draw(self):
        self.image.clip_draw()