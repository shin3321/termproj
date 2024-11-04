from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_z, SDLK_s, SDLK_w, SDLK_LSHIFT, SDLK_x


def start_event(e):
    return e[0] == 'START'

def space_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_SPACE)

def time_out(e):
    return e[0] == 'TIME_OUT'

def d_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_d)
def d_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_d)
def a_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_a)
def a_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_a)

def s_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_s)
def s_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_s)

def w_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_w)
def w_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_w)

def lshift_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_LSHIFT)

def lshift_up (e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_LSHIFT)

#공격 모션
def z_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_z)
def z_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_z)

def x_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_x)
def x_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_x)





class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            e = self.event_que.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.o, e)
                    print(f'    exit from{self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'    enter into {self.cur_state}')
                    return


    def start(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter(self.o, ('START', 0))  # 더미 이벤트
        print(f'    enter into {self.cur_state}')

    def draw(self, o):
        self.cur_state.draw(self.o)