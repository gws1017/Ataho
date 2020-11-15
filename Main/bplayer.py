import random
from random  import randint
from pico2d import *
import gfw
from gobj import *
from math import *

SKILL_NAME = ["tigerfist","lightslash"]

EFFECT_NAME = ["ready","punch","impossible","lightcollect","hit"]

IMAGE_SX = {
    SKILL_NAME[0] : [0,48,97,160,219,283],
    SKILL_NAME[1] : [353,450],
    "energy2" : [49,96,146,0]
    }
IMAGE_WIDTH = {
    SKILL_NAME[0] : [48,48,54,58,64,53],
    SKILL_NAME[1] : [47,54],
    "energy2" : [32,32,28,32]
    }
LIGHT_LEVEL = {
    0 : [(0,0,12,15,130+35,298,12,15),
         (12,0,23,15,130+41,298-7,350,15),
         (35,0,11,15,130+391,298-7)
        ],
    1 : [(0,0,12,16,130+35,298,12,16),
         (12,0,23,16,130+41,298 - 8,350,16),
         (35,0,13,16,130+391,298-8)
        ],
    2 : [(0,0,16,32,130+35,298,16,32),
         (16,0,17,32,130+43,298-16,350,32),
         (33,0,15,32,130+393,298-16)
        ],
    3 : [(0,0,30,64,130+35,298,30,64),
         (30,0,19,64,130+50,298-32,350,64),
         (49,0,26,64,130+400,298-32)
        ]
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
        self.image2 = gfw.image.load(res('at_victory.png'))

    def enter(self,st,st2): #각 스테이트에 진입(enter)될때마다 처리(초기화)해야하기 때문에 엔터 함수를 추가함
        self.st = st
        self.st2 = st2
        self.time = 0 #타임 변수 추가
        self.fidx = 0
        self.action = 2
        self.endtime = 0
        
        self.wav = load_wav('./res/bgm/'+ EFFECT_NAME[2] +'.wav')
        self.wav2 = [load_wav('./res/bgm/'+ EFFECT_NAME[4] +'.wav')]
        
    def exit(self): #스테이트를 빠져 나갈때 할것
        pass
    def draw(self):

        width,height = 48,64
        sx = self.fidx * width
        sy = self.action * height
        if self.endtime > 0 :
            print(self.fidx)
            sx = self.fidx * width
            self.image2.clip_draw(sx, 0, width, 64, *self.player.pos)
        else : self.image.clip_draw(sx, sy, width, height, *self.player.pos)

    def update(self): 

        if self.player.monster.dead == 1 and self.endtime == 0:
            self.player.STATUS["curExp"] += self.player.monster.STATUS["curExp"]
            self.endtime += gfw.delta_time*5
        if self.endtime > 0 :
            self.endtime += gfw.delta_time*5
            self.fidx = int(self.endtime) % 6
            if self.endtime >=2 and self.endtime < 2.1 :
                self.player.bgm2.play(1)
        if self.endtime > 25 :
            return -1
                        
        if self.player.hit == 1 :
            self.player.hit = 2
            m=self.player.monster
            dmg = m.STATUS["atk"] - self.player.STATUS["df"]
            self.player.STATUS["curHp"] = self.player.STATUS["curHp"] - dmg
            if self.player.STATUS["curHp"] < 0:
                self.player.STATUS["curHp"] = 0
            if self.player.STATUS["curHp"] == 0 :
                self.player.set_state(DeadState)
            if dmg == 0:
                self.fidx = 2
            else : self.fidx = 1
        if self.player.hit == 2:
            self.time += gfw.delta_time # 업데이트 될때마다 시간을 더해줌 (객체가 생성된 이후로 흐른 시간)
            frame = self.time * 5
            if frame < 3 and self.fidx == 1:
                if frame >=0 and frame < 0.1:
                    self.wav2[0].play(1)
            else :
                self.fidx = 0
                self.player.hit = 0
        

        move_obj(self.player)
        return False
        

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair == Player.KEYDOWN_SPACE:
            if self.player.st == 1:
                s = self.player.STATUS
                if self.player.st2 == 0:
                    if s["curMp"] < self.player.manaconsum[0] :
                        self.wav.play(1)
                        return
                    else : s["curMp"] = s["curMp"] - self.player.manaconsum[0]
                elif self.player.st2 == 1:
                    if s["curMp"] < self.player.manaconsum[1] :
                        self.wav.play(1)
                        return
                    else : s["curMp"] = s["curMp"] - self.player.manaconsum[1]
            self.player.set_state(FireState)

class DeadState:
    @staticmethod
    def get(player):
        if not hasattr(DeadState, 'singleton'):  #싱글턴이라는 멤버를 가지고있냐?(hasattr함수/파이썬 기본함수) 없으면
            DeadState.singleton = DeadState() #만들자
            DeadState.singleton.player = player
        return DeadState.singleton  #있으면 리턴

    def __init__(self):
        self.image = gfw.image.load(res('at_btl.png'))

    def enter(self,st,st2): #각 스테이트에 진입(enter)될때마다 처리(초기화)해야하기 때문에 엔터 함수를 추가함
        self.time = 0 #타임 변수 추가
        self.fidx = 0
        self.sx = [336,416,496]
        self.width = [73,76,70]
        self.action = 2

        
    def exit(self): #스테이트를 빠져 나갈때 할것
        pass
    def draw(self):
        sx = self.sx[self.fidx]
        width = self.width[self.fidx]
        height = 58
        x,y = self.player.pos
        self.image.clip_draw(sx, 0, width, height, x - self.fidx * 0.9,y)

    def update(self): 
        self.time += gfw.delta_time # 업데이트 될때마다 시간을 더해줌 (객체가 생성된 이후로 흐른 시간)
        frame = self.time * 8
        print(self.time)
        self.fidx = int(frame) % 3
        if self.time > 10 :
            return -1
        else : return -2
        

        move_obj(self.player)
        return False
        

    def handle_event(self, e):
        pair = (e.type, e.key)
        


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
        self.image3 = [gfw.image.load(res(SKILL_NAME[1] + '1.png')),
                       gfw.image.load(res(SKILL_NAME[1] + '2.png')), 
                       gfw.image.load(res(SKILL_NAME[1] + '3.png')),
                       gfw.image.load(res(SKILL_NAME[1] + '4.png')),  
                      ] #광선 이미지
        self.image4 = gfw.image.load(res('energy.png'))
        self.image5 = gfw.image.load(res('energy2.png'))
        self.WAV_LIST = {
         SKILL_NAME[0] : [load_wav('./res/bgm/'+ SKILL_NAME[0] +'.wav')], #호랑이 소리
         SKILL_NAME[1] : [load_wav('./res/bgm/'+ SKILL_NAME[1] +'.wav')], #광선 쏘는 소리
         EFFECT_NAME[0] : [load_wav('./res/bgm/'+ EFFECT_NAME[0] +'.wav')],#팔 휘적거리는소리
         EFFECT_NAME[1] : [load_wav('./res/bgm/'+ EFFECT_NAME[1] +'.wav')],#펀치 소리
         EFFECT_NAME[3] : [load_wav('./res/bgm/'+ EFFECT_NAME[3] +'.wav')],#에너지 모으는 소리
         }

    def enter(self,st,st2):
        self.st = st
        self.st2 = st2
        self.pos = 130,300
        self.time = 0
        if self.st == 0 and self.st2 == 0:
            self.action = 1
            self.fidx = 0
        elif self.st == 1 and self.st2 == 0:
            self.fidx = 0
            self.action = 0
            self.winkle = False
        elif self.st == 1 and self.st2 == 1:
            self.fidx = 0
            self.fidx5 = 3
            self.action = 1
            self.r = [randint(30,80) for _ in range(50)]
            self.angle = [randint(0,360) for _ in range(50)]
        elif self.st == 3 and self.st2 == 0:
            self.fidx = 3
            self.action = 2
        elif self.st == 3 and self.st2 == 1:
            self.fidx = 2
            self.action = 2


    def exit(self):
        pass
    def draw(self):
        height = 64
        x,y = self.pos
        if self.st == 0 and self.st2 == 0:
            width = 64
            sx = self.fidx * width
            sy = self.action * height
            self.image.clip_draw(sx, sy, width, height, x, y)

        elif self.st == 1 and self.st2 == 0:
            width = IMAGE_WIDTH["tigerfist"][self.fidx]
            sx = IMAGE_SX["tigerfist"][self.fidx]
            sy = self.action * height
            self.image.clip_draw(sx, sy, width, height, x, y)
            if self.fidx == 5 and self.winkle == False:
                self.image2.clip_draw(0,0,self.image2.w,self.image2.h,x+300,y)
        elif self.st == 1 and self.st2 == 1:
            width = IMAGE_WIDTH["lightslash"][self.fidx]
            sx = IMAGE_SX["lightslash"][self.fidx]
            sy = self.action * height
            self.image.clip_draw(sx, sy, width, height, x, y)
            if self.fidx == 0 :
                if self.r[0] == 0 :
                    width5 = IMAGE_WIDTH["energy2"][int(self.fidx5)]
                    sx5 = IMAGE_SX["energy2"][int(self.fidx5)]
                    self.image5.clip_draw(sx5,0,width5,30,x-20,y-5)
                for i in range(50) :
                    if i < 25:
                        rx,ry = cos(radians(self.angle[i]))*radians(self.angle[i])*self.r[i],sin(radians(self.angle[i]))*radians(self.angle[i])*self.r[i]
                    else :
                        rx,ry = cos(radians(self.angle[i]))*self.r[i],sin(radians(self.angle[i]))*self.r[i]
                    cx = x-20
                    cy = y-5
                    self.image4.draw(cx + rx,cy + ry)
                
            if self.fidx == 1 :
                level = self.player.slevel["lightslash"][0]-1
                rect = LIGHT_LEVEL[level]
                height = self.image3[0].h
                self.image3[level].clip_draw(*rect[0])
                self.image3[level].clip_draw_to_origin(*rect[1])
                self.image3[level].clip_draw_to_origin(*rect[2])

        elif self.st == 3 :
            width = 48
            sx = self.fidx * width
            sy = self.action * height
            self.image.clip_draw(sx, sy, width, height, x, y)
            

        

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 5
        if self.st == 0 and self.st2 == 0:
            if frame < 2:
                self.fidx = int(frame)
                if frame >= 1 and frame < 1.1 : self.WAV_LIST["punch"][0].play(1)
            else:
                self.player.set_state(IdleState)
        elif self.st == 1 and self.st2 == 0: 
            if frame < 6:
                self.fidx = int(frame)
                if frame >= 2 and frame < 2.1 : self.WAV_LIST["ready"][0].play(3)
            elif frame >=6 and frame < 15 :
                if frame >= 6 and frame < 6.1 : self.WAV_LIST["tigerfist"][0].play(1)
                point = frame - int(frame)
                if  frame >=10 and point >= 0 and point <= 0.5:
                    self.winkle = True
                else :self.winkle = False
            else:
                self.player.set_state(IdleState)
        elif self.st == 1 and self.st2 == 1:
            if frame < 35:
                if frame < 20 :
                    self.fidx = 0
                    
                    if self.r[0] == 0 :
                        if self.fidx5 <= 0 : self.fidx5 = 3
                        self.fidx5 -= gfw.delta_time * 5
                    for i in range(50):
                        if self.r[i] > 0 : self.r[i] = self.r[i] -0.5
                        if self.angle[i] > 0 : self.angle[i] = self.angle[i] -0.5
                    if frame >= 0 and frame < 0.1 : self.WAV_LIST["lightcollect"][0].play(1)
                elif frame >= 20 and frame < 35 :
                    if frame >= 20 and frame < 20.1 : self.WAV_LIST["lightslash"][0].play(1)
                    self.fidx = 1
            else:
                self.player.set_state(IdleState)
        elif self.st == 3 and self.st2 == 0:
            x,y = self.pos
            x = x-1
            self.pos = x,y
            self.player.pos = x,y
            if self.player.pos[0] <= -48:
                return -1
        elif self.st == 3 and self.st2 == 1:
            if frame < 5:
                pass
            else:
                self.player.set_state(IdleState)
        return True

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
    
    #constructor
    def __init__(self):
        # self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.pos = 130, 300
        self.delta = 0, 0
        self.fidx = 0
        self.target = None
        self.targets = []
        self.speed = 0
        self.time = 0
        self.state = None
        self.st = 0
        self.st2 = 0
        self.hit = 0
        self.dead = False
        self.name = "아타호"
        self.set_state(IdleState)
        self.image = gfw.image.load(res('at_btl.png'))
        self.manaconsum = [7,12]
        self.slevel = {
        SKILL_NAME[0]: [1,0],
        SKILL_NAME[1]: [4,0]
        }
        self.STATUS = {
            "lvl" : 1,
            "curHp" : 30,
            "curMp" : 30,
            "curExp" : 0,
            "maxHp" : 30,
            "maxMp" : 30,
            "maxExp" : 100,
            "atk" : 22,
            "df" : 17,
            "act" : 20,
        }
        self.PLAYER_SINFO = {
          (0,0) :  self.STATUS["atk"],
          (1,0) :  self.STATUS["atk"]*(self.slevel["tigerfist"][0]*0.1+1),
          (1,1) :  self.STATUS["atk"]*(self.slevel["lightslash"][0]*0.1+1),
          (2,0) : 0,
          (3,0) : 0,
          (3,1) : 0
        }
        

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter(self.st,self.st2)

    #현재 스테이트에 따라 draw update fire handle_event 를 하도록
    def draw(self):
        self.state.draw()

    def update(self):
        s = self.STATUS
        if s["curExp"] == 100 :
            s["maxHp"] +=  randint(2,5)
            s["maxMp"] +=  randint(2,5)
            s["atk"] += randint(2,5)
            s["df"] += randint(2,5)
            s["act"] += randint(2,5)
            s["curExp"] = 0
            s["curHp"] = s["maxHp"]
            s["curMp"] = s["maxMp"]
            s["lvl"] += 1
        return self.state.update()

    def fire(self):
        self.time = 0
        self.set_state(FireState) #파이어 스테이트로 바뀜

    def handle_event(self, e):
        self.state.handle_event(e)
