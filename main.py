import pico2d

import finale
import game_mode
import game_framework
from pico2d import *
import logo_mode
import title_mode

screen_width, screen_height = 1200, 800

pico2d.open_canvas(screen_width, screen_height)
game_framework.run(logo_mode)
  
pico2d.clear_canvas()
