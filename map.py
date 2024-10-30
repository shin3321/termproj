from pico2d import *

screen_width, screen_height = 1200, 800
world_width, world_height = 2000, 2000
back_wid, back_height = 200, 400


def draw_background(cx, cy):
    # 화면에 그려질 배경 타일의 시작과 끝 위치를 계산합니다.
    start_x = max(0, cx - screen_width // 2)
    end_x = min(world_width, cx + screen_width // 2 + back_wid)
    start_y = max(0, cy - screen_height // 2)
    end_y = min(world_height, cy + screen_height // 2 + back_height)

    background = load_image('img/Dwelling_Tiles.png')

    # x 범위와 y 범위에 맞게 타일을 그립니다.
    for x in range(start_x, end_x, back_wid):
        for y in range(start_y, end_y, back_height):
            background.clip_draw(0, 644, 508, 892, x - cx + screen_width // 2, y - cy + screen_height // 2, back_wid,
                                 back_height)


open_canvas(screen_width, screen_height)