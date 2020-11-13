import random
from pico2d import *
import gfw
from gobj import *

SKILL_NAME = ["tfist","ready"]

IMAGE_SX = {
    SKILL_NAME[0] : [0,48,97,160,219,283]
    }
IMAGE_WIDTH = {
    SKILL_NAME[0] : [48,48,54,58,64,53]
    }


class IdleState:
    @staticmethod
    def get(player):
        if not hasattr(IdleState, 'singleton'):  #싱글턴이라는 멤버를 가지고있냐?(hasattr함수/파이썬 기본함수) 없으면
            IdleState.singleton = IdleState() #만들자
            IdleState.singleton.player = player
        return IdleState.singleton  #있으면 리턴

    def __init__(self):
        self.image = gfw.image.load(res('at_btl.png'))

    def enter(self): #각 스테이트에 진입(enter)될때마다 처리(초기화)해야하기 때문에 엔터 함수를 추가함
        self.time = 0 #타임 변수 추가
        self.fidx = 0
        self.action = 2
    def exit(self): #스테이트를 빠져 나갈때 할것
        pass
    def draw(self):
        width,height = 48,64
        sx = self.fidx * width
        sy = self.action * height
        self.image.clip_draw(sx, sy, width, height, *self.player.pos)

    def update(self):
        self.time += gfw.delta_time # 업데이트 될때마다 시간을 더해줌 (객체가 생성된 이후로 흐른 시간)
        # self.player.pos = point_add(self.player.pos, self.player.delta)
        move_obj(self.player)
        return True
        

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair == Player.KEYDOWN_SPACE:
            self.player.set_state(FireState)


class FireState:
    @staticmethod
    def get(player):
        if not hasattr(FireState, 'singleton'): #idlestate와 동일
            FireState.singleton = FireState()
            FireState.singleton.player = player
        return FireState.singleton

    def __init__(self):
        self.image = gfw.image.load(res('at_btl.png'))
        self.image2 = gfw.image.load(res('tiger_fist.png'))
        self.WAV_LIST = {
         SKILL_NAME[0] : [load_wav('./res/bgm/tigerfist.wav')],
         SKILL_NAME[1] : [load_wav('./res/bgm/'+ SKILL_NAME[1] +'.wav')]
         }

    def enter(self):
        self.pos = 130,300
        self.time = 0
        self.fidx = 0
        self.action = 0
        self.winkle = False


    def exit(self):
        pass
    def draw(self):
        height = 64
        width = IMAGE_WIDTH["tfist"][self.fidx]
        sx = IMAGE_SX["tfist"][self.fidx]
        sy = self.action * height
        x,y = self.pos
        self.image.clip_draw(sx, sy, width, height, x, y)
        if self.fidx == 5 and self.winkle == False:
            self.image2.clip_draw(0,0,self.image2.w,self.image2.h,x+300,y)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 5
        print(frame)
        if frame < 6:
            self.fidx = int(frame)
            if frame >= 2 and frame < 2.1 : self.WAV_LIST["ready"][0].play(3)
        elif frame >=6 and frame < 15 :
            if frame >= 6 and frame < 6.1 : self.WAV_LIST["tfist"][0].play(1)
            point = frame - int(frame)
            if  frame >=10 and point >= 0 and point <= 0.5:
                self.winkle = True
            else :self.winkle = False
        else:
            self.player.set_state(IdleState)
        return False

    def handle_event(self, e):
        pass

class Player:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT): ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):  ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):    ( 0,  1),
        (SDL_KEYUP, SDLK_LEFT):    ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):   (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):    ( 0,  1),
        (SDL_KEYUP, SDLK_UP):      ( 0, -1),
    }
    KEYDOWN_SPACE = (SDL_KEYDOWN, SDLK_SPACE)
    image = None
    STATUS = {
        "lvl" : 1,
        "curHp" : 15,
        "curMp" : 30,
        "curExp" : 0,
        "maxHp" : 30,
        "maxMp" : 30,
        "maxExp" : 100,
        "atk" : 22,
        "df" : 17,
        "act" : 20,
    }
    #constructor
    def __init__(self):
        # self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.pos = 130, 350
        self.delta = 0, 0
        self.fidx = 0
        self.target = None
        self.targets = []
        self.speed = 0
        self.time = 0
        self.state = None
        self.name = gfw.font.load(RES_DIR + '/neodgm.ttf', 18)
        self.set_state(IdleState)
        self.image = gfw.image.load(res('at_btl.png'))

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    #현재 스테이트에 따라 draw update fire handle_event 를 하도록
    def draw(self):
        self.state.draw()

    def update(self):
        return self.state.update()

    def fire(self):
        self.time = 0
        self.set_state(FireState) #파이어 스테이트로 바뀜

    def handle_event(self, e):
        self.state.handle_event(e)
