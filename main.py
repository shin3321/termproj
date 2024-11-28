import pico2d

import game_mode
import game_framework
from pico2d import *
import logo_mode
screen_width, screen_height = 1200, 800

pico2d.open_canvas(screen_width, screen_height)
game_framework.run(game_mode)
  
pico2d.clear_canvas()
