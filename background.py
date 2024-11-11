from cgi import print_environ_usage

import server

from pico2d import *

screen_width, screen_height = 1200, 800
world_width, world_height = 2000, 2000
back_wid, back_height = 200, 400

#
# def draw_background(cx, cy):
#     # 화면에 그려질 배경 타일의 시작과 끝 위치를 계산합니다.
#     start_x = max(0, cx - screen_width // 2)
#     end_x = min(world_width, cx + screen_width // 2 + back_wid)
#     start_y = max(0, cy - screen_height // 2)
#     end_y = min(world_height, cy + screen_height // 2 + back_height)
#
#     background = load_image('img/Dwelling_Tiles.png')
#
#     # x 범위와 y 범위에 맞게 타일을 그립니다.
#     for x in range(start_x, end_x, back_wid):
#         for y in range(start_y, end_y, back_height):
#             background.clip_draw(0, 644, 508, 892, x - cx + screen_width // 2, y - cy + screen_height // 2, back_wid,
#                                  back_height)

class Background():
    def __init__(self):
        self.image =  load_image('img/lv1backgrounds.png')
        self.cw = get_canvas_width()
        print(f'{self.cw}')
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

        pass


    def draw(self):
        for x in range(0, self.cw, self.w):  # 캔버스 너비만큼 반복
            for y in range(0, self.ch, self.h):  # 캔버스 높이만큼 반복
                self.image.draw_to_origin(x, y)  # 이미지 원본 크기로 그리기

    def update(self):
        self.window_left = clamp(0, int(server.hero.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.hero.y) - self.ch // 2, self.h - self.ch - 1)
        pass


    def clear(self):

        pass

# class TileBackGround:
#     def __init__(self):
#         self.cw = get_canvas_width()
#         self.ch = get_canvas_height()
#         self.w = 800 * 3
#         self.h = 600 * 3
#
#         self.tiles = [[load_image('img/lv1backgrounds%d%d.png' %(x, y)) for x in range(3)] for y in range(3) ]
#
#     def draw(self):
#         self.window_left = clamp(0, int(server.boy.x) - self.cw // 2, self.w - self.cw - 1)
#         self.window_bottom = clamp(0, int(server.boy.y) - self.ch // 2, self.h - self.ch - 1)
#         tile_left = self.window_left // 800
#         tile_right = (self.window_left + self.cw) // 800
#         left_offset = self.window_left % 800
#         tile_bottom = self.window_bottom // 600
#         tile_top = (self.window_bottom + self.ch) // 600
#         bottom_offset = self.window_bottom % 600
#         for ty in range(tile_bottom, tile_top + 1):
#             for tx in range(tile_left, tile_right + 1):
#                 self.tiles[ty][tx].draw_to_origin(-left_offset + (tx - tile_left) * 800,                                                      -bottom_offset + (ty - tile_bottom) * 600)