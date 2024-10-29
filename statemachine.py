from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_d


def space_down(e):
    return (e[0] == 'INPUT' and e[1] == SDL_KEYDOWN
            and e[1].key == SDLK_SPACE)

def time_out(e):
    return e[0] == 'TIME_OUT'

def D_down(e):
    return e[0] == 'INPUT' and e[1] == SDL_KEYDOWN and e[1].key == SDLK_d

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
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    return


    def start(self, start_state):
        self.cur_state = start_state


    def draw(self, o):
        self.cur_state.draw(self.o)