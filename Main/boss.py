import random
from pico2d import *
import gfw
from gobj import *

IMG_INFO ={
    0 : [],
    1 : []
}


class IdleState:
    @staticmethod
    def get(Boss):
        if not hasattr(IdleState, 'singleton'): 
            IdleState.singleton = IdleState()
            IdleState.singleton.Boss = Boss
        return IdleState.singleton

    def __init__(self):
        pass

    def enter(self,st,st2):
        self.time = 0
        self.fidx = 0
        self.hit = 0
        self.deadtime = 0
        self.image = self.Boss.image
        self.stoptime = {
         (0,0) : 5,
         (1,0) : 10,
         (1,1) : 18,   
        }
        self.sx = 0
        self.width = (48,54)
       

    def exit(self):
        pass
    def draw(self):

        p = self.Boss.player
        
        width = self.width[0]
        width2 = self.width[1]
        sx = width * self.fidx
        if self.Boss.dead == False :
            if self.hit == 0:
                self.Boss.image.clip_draw(sx, 304, width, 96, *self.Boss.pos)
            elif self.hit != 0 :
                stop = self.stoptime[(p.st,p.st2)]               
                if p.st == 0 and p.st2 == 0  : 
                    self.Boss.image.clip_draw(sx, 304, width2, 96, *self.Boss.pos)
                elif p.st == 1 and p.st2 == 0  : 
                    if self.time > 6 :
                        self.Boss.image.clip_draw(sx, 304, width2, 96, *self.Boss.pos)
                    elif self.time <= 6 : self.Boss.image.clip_draw(0, 304, width, 96, *self.Boss.pos)
                elif p.st == 1 and p.st2 == 1  : 
                    if self.time > 10 :
                        self.Boss.image.clip_draw(sx, 304, width2, 96, *self.Boss.pos)
                    elif self.time <= 10 : self.Boss.image.clip_draw(0, 304, width, 96, *self.Boss.pos)
                elif p.st == 3 and p.st2 == 1  : 
                    self.Boss.image.clip_draw(0, 304, width, 96, *self.Boss.pos)
                if self.time > stop and self.deadtime == 0 :
                    if p.st == 3 and p.st2 == 0: return
                    self.Boss.set_state(FireState)



    def update(self,data):
        self.Boss = data
        self.time +=  gfw.delta_time * 5
        if self.Boss.STATUS["curHp"] == 0 : 
            self.deadtime += gfw.delta_time * 5
        if self.deadtime > 10 : 
            self.Boss.dead = True
            return -3
        p = self.Boss.player
        m = self.Boss
        if self.Boss.DRAW == False and self.hit == 0:
            if p.st != 3 : 
                self.hit += 1
                self.fidx += 1
            dmg = p.PLAYER_SINFO[(p.st,p.st2)] - m.STATUS["df"]
            if int(dmg) < 0 : dmg = 0
            m.STATUS["curHp"] = m.STATUS["curHp"] - int(dmg)
            
        elif self.Boss.DRAW == True: self.hit,self.time = 0,0

        if m.STATUS["curHp"] < 0 : m.STATUS["curHp"] = 0


        return False

    def handle_event(self, e):
        pair = (e.type, e.key)
        

class FireState:
    @staticmethod
    def get(Boss):
        if not hasattr(FireState, 'singleton'): 
            FireState.singleton = FireState()
            FireState.singleton.Boss = Boss
        return FireState.singleton

    def __init__(self):
        pass

    def enter(self,st,st2):
        self.time = 0
        self.fidx = 0
        self.fidx2 = 0
        self.Boss.skill = random.randint(0,1)
        self.image = self.Boss.image
        self.fog = gfw.image.load(res('fog.png'))
        self.sx = [[468,0,90,170,271,350,448],[118,171,235,315,395]]
        self.width = [[48,90,80,101,79,98,96],[53,64,80,80,54]]
        self.height = [[96,87,87,87,87,87,87],[95,95,95,95,95]]  
        self.action = [[304,210,210,210,210,210,210],[304,304,304,304,304]]
        self.fsx = [0,46,92,138,189]
        self.fwidth = [46,46,46,51,44]


    def exit(self):
        pass
    def draw(self):
        sx = self.sx[self.Boss.skill][self.fidx]
        sy = self.action[self.Boss.skill][self.fidx]
        width = self.width[self.Boss.skill][self.fidx]
        height = self.height[self.Boss.skill][self.fidx]
        x,y = self.Boss.pos
        self.image.clip_draw(sx, sy, width, height, x, y)
        sx = self.fsx[self.fidx2]
        width = self.fwidth[self.fidx2]
        x,y = self.Boss.player.pos
        if self.Boss.skill == 1:
            self.fog.clip_draw(sx, 0, width, 27, x-15, y-20)
            self.fog.clip_draw(sx, 0, width, 27, x, y-20)
            self.fog.clip_draw(sx, 0, width, 27, x+15, y-20)
            self.fog.clip_draw(sx, 0, width, 27, x-15, y-6)
            self.fog.clip_draw(sx, 0, width, 27, x, y-6)
            self.fog.clip_draw(sx, 0, width, 27, x+15, y-6)
            self.fog.clip_draw(sx, 0, width, 27, x-15, y+7)
            self.fog.clip_draw(sx, 0, width, 27, x, y+7)
            self.fog.clip_draw(sx, 0, width, 27, x+15, y+7)

    def update(self,data):
        self.time += gfw.delta_time
        frame = self.time * 5
        frame2 = self.time * 10

        if self.Boss.skill == 0:
            mf =7
        else : mf = 5

        if frame < mf:
            self.fidx = int(frame)
            self.fidx2 = int(frame2) % 5
        else:
            #플레이어에게 정보전달을 해야함
            self.Boss.set_state(IdleState)
            return True

    def handle_event(self, e):
        pass

class Boss:
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
        self.pos = 500, 300
        self.delta = 0, 0
        self.fidx = 0
        self.target = None
        self.targets = []
        self.speed = 0
        self.time = 0
        self.isBoss = None
        self.st = 0
        self.st2 = 0
        self.monster = None
        self.state = None
        self.DRAW = True
        self.dead = False
        self.set_state(IdleState)
        self.image = gfw.image.load(res('boss.png') )
        self.name = "보스"
        self.skill = 0
        self.STATUS = {
            "lvl" : 1,
            "curHp" : 100,
            "curMp" : 30,
            "curExp" : 10,
            "maxHp" : 100,
            "maxMp" : 30,
            "maxExp" : 100,
            "atk" : 50,
            "df" : 60,
            "act" : 15,
        }

    def set_isBoss(self):
        pass

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        
        self.state.enter(self.st,self.st2)

    def draw(self):
        self.state.draw()

    def update(self,D):
        self.DRAW = D
        return self.state.update(self)

    def fire(self):
        self.time = 0
        self.set_state(FireState)

    def handle_event(self, e):
        self.state.handle_event(e)
    def get_state(self):
        return self.state
