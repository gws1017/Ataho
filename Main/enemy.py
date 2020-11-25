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
    def get(monster):
        if not hasattr(IdleState, 'singleton'): 
            IdleState.singleton = IdleState()
            IdleState.singleton.monster = monster
        return IdleState.singleton

    def __init__(self):
        pass
    def reset(self,mon):
        self.monster = mon

    def enter(self,st,st2):
        if self.monster.type == 0 :
            self.sx = 115
            self.width = (37,37)
        elif self.monster.type == 1:
            self.sx = 131
            self.width = (56,69)
        self.time = 0
        self.fidx = 0
        self.hit = 0
        self.deadtime = 0
        self.image = self.monster.image
        self.stoptime = {
         (0,0) : 5,
         (1,0) : 10,
         (1,1) : 18,
         (3,0) : 0,
         (3,1) : 5,  
        }
        
        

    def exit(self):
        pass

    def draw(self):

        p = self.monster.player
        sx = self.sx
        width = self.width[0]
        width2 = self.width[1]
        if self.monster.dead == False :
            if self.hit == 0:
                self.monster.image.clip_draw(0, 0, width, 64, *self.monster.pos)
            elif self.hit != 0 :
                stop = self.stoptime[(p.st,p.st2)]            
                if p.st == 0 and p.st2 == 0  : 
                    self.monster.image.clip_draw(sx, 0, width2, 64, *self.monster.pos)
                elif p.st == 1 and p.st2 == 0  : 
                    if self.time > 6 :
                        self.monster.image.clip_draw(sx, 0, width2, 64, *self.monster.pos)
                    elif self.time <= 6 : self.monster.image.clip_draw(0, 0, width, 64, *self.monster.pos)
                elif p.st == 1 and p.st2 == 1  : 
                    if self.time > 10 :
                        self.monster.image.clip_draw(sx, 0, width2, 64, *self.monster.pos)
                    elif self.time <= 10 : self.monster.image.clip_draw(0, 0, width, 64, *self.monster.pos)
                elif p.st == 3 and p.st2 == 1  :  
                    self.monster.image.clip_draw(0, 0, width, 64, *self.monster.pos)
                if self.time > stop and self.deadtime == 0 :
                    if p.st == 3 and p.st2 == 0: return
                    self.monster.set_state(FireState)




    def update(self,data):
        self.monster = data
        self.time +=  gfw.delta_time * 5
        if self.monster.STATUS["curHp"] == 0 : 
            self.deadtime += gfw.delta_time * 5
        if self.deadtime > 10 : 
            self.monster.dead = True
        p = self.monster.player
        m = self.monster
        if self.monster.DRAW == False and self.hit == 0:
            self.hit += 1
            dmg = p.PLAYER_SINFO[(p.st,p.st2)] - m.STATUS["df"]
            if int(dmg) < 0 : dmg = 0
            m.STATUS["curHp"] = m.STATUS["curHp"] - int(dmg)
            
        elif self.monster.DRAW == True: self.hit,self.time = 0,0

        if m.STATUS["curHp"] < 0 : m.STATUS["curHp"] = 0

        return False

    def handle_event(self, e):
        pair = (e.type, e.key)
        

class FireState:
    @staticmethod
    def get(monster):
        if not hasattr(FireState, 'singleton'): 
            FireState.singleton = FireState()
            FireState.singleton.monster = monster
        return FireState.singleton

    def __init__(self):
        pass

    def reset(self,mon):
        self.monster = mon

    def enter(self,st,st2):
        self.time = 0
        self.fidx = 0
        self.image = self.monster.image
       

    def exit(self):
        pass
    def draw(self):
        if self.monster.type == 0 :
            sx = 39
            width = 52
        elif self.monster.type == 1:
            sx = 57
            width = 68
        
        x,y = self.monster.pos
        self.image.clip_draw(sx, 0, width, 64, x, y)

    def update(self,data):
        self.monster = data
        self.time += gfw.delta_time
        frame = self.time * 5
        
        if frame < 5:
            pass
        else:
            #플레이어에게 정보전달을 해야함
            self.monster.set_state(IdleState)
            return True

    def handle_event(self, e):
        pass

class Monster:
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
    def __init__(self,tp):
        # self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.pos = 500, 300
        self.mob = None
        self.delta = 0, 0
        self.fidx = 0
        self.target = None
        self.targets = []
        self.speed = 0
        self.time = 0
        self.st = 0
        self.st2 = 0
        self.state = None
        self.type = tp
        self.DRAW = True
        self.dead = False
        self.set_state(IdleState)
        if tp == 0 :
            self.image = gfw.image.load(res('monkey.png') )
            self.name = "원숭이"
            self.STATUS = {
            "lvl" : 1,
            "curHp" : 15,
            "curMp" : 30,
            "curExp" : 10,
            "maxHp" : 15,
            "maxMp" : 30,
            "maxExp" : 100,
            "atk" : 20,
            "df" : 12,
            "act" : 15,
        }
        elif tp == 1:
            self.image = gfw.image.load(res('skeleton.png') )
            self.name = "해골"
            self.STATUS = {
            "lvl" : 10,
            "curHp" : 65,
            "curMp" : 30,
            "curExp" : 40,
            "maxHp" : 65,
            "maxMp" : 30,
            "maxExp" : 100,
            "atk" : 48,
            "df" : 53,
            "act" : 15,
        }
        

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter(self.st,self.st2)

    def draw(self):
        self.state.draw()

    def update(self,D):
        self.state.reset(self)
        self.DRAW = D
        return self.state.update(self)

    def fire(self):
        self.time = 0
        self.set_state(FireState)

    def handle_event(self, e):
        self.state.handle_event(e)
    def get_state(self):
        return self.state
