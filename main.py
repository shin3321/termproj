import game_mode
import game_framework
from pico2d import *
import logo_mode

pico2d.open_canvas()
game_framework.run(logo_mode)
pico2d.close_canvas()

while game_mode.Running:
    game_mode.handle_event()

    # cx = character.x - screen_width //2
    # cy = character.y - screen_height//2

    # cx = max(0, min(cx, world_width - screen_width))
    # cy = max(0, min(cy, world_height - screen_height))
    # draw_background(cx, cy)
    game_mode.update()
    game_mode.draw()
    #update_canvas()
    delay(0.001)

game_mode.finish()
close_canvas()