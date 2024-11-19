from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_z, SDLK_s, SDLK_w, SDLK_LSHIFT, SDLK_x


def start_event(e):
    return e[0] == 'START'

def walk(e):
    return e[0] == 'WALK'

def idle(e):
    return e[0] == 'IDLE'

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

def space_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN
            and e[1].key == SDLK_SPACE)


def space_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP
            and e[1].key == SDLK_SPACE)

def changeHp(e):
    return e[0] == 'CHANGE'



class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []
        self.active_states = set()

    def add_event(self, e):
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        for state in self.active_states:
            state.do(self.o)

        if self.event_que:

            for state in list(self.active_states):
                e = self.event_que.pop(0)
                for check_event, next_state in self.transitions[state].items():
                    if check_event(e):
                        state.exit(self.o, e)
                        print(f'    exit from{state}')
                        self.active_states.discard(state)

                        self.active_states.add(next_state)
                        next_state.enter(self.o, e)
                        print(f'    enter into {next_state}')
                        break


    def start(self, start_states):
        for state in start_states:
            self.active_states.add(state)
            state.enter(self.o, ('START', 0))  # 더미 이벤트
            print(f'    enter into {state}')

    def draw(self, o):
        for state in self.active_states:
            state.draw(self.o)