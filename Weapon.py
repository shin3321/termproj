from pico2d import *
img_size = 128

class Bomb: #(1, 6)
    image = None
    gravity = -0.3
    def __init__(self, x, y, velocity):
        if Bomb.image == None:
            self.image = load_image('img/items.png')
        self.x, self.y = x, y
        self.velocity_x = velocity * 5
        self.velocity_y = velocity

    def draw(self):
        print(f'draw bomb{self.x}{self.y}')
        self.image.clip_draw(img_size*0, img_size*10, img_size,img_size,self.x, self.y, 50, 50)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += Bomb.gravity

