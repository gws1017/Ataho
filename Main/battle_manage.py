import gfw
import gobj
from pico2d import *
from bplayer import Player

class BattleManager:
    def __init__(self):
        self.image = gfw.image.load(gobj.res('skillwindow.png'))
        self.select1 = gfw.image.load(gobj.res('select1.png'))
        self.select2 = gfw.image.load(gobj.res('select2.png'))
        self.slist = [[gfw.image.load(gobj.res('skill1.png'))],
                      [],
                      [gfw.image.load(gobj.res('run.png')),gfw.image.load(gobj.res('defense.png'))] ]


        self.pos = 200,128
        self.spos = 217 + self.select1.w // 2,409 - self.select1.h
        self.spos2 = 225 - self.select2.w ,336 - self.select1.h
        self.stidx = 0
        self.sname = gfw.font.load(gobj.RES_DIR + '/neodgm.ttf', 18)
        self.player = Player()
        self.st2idx = 0
        self.sname = gfw.font.load(gobj.RES_DIR + '/neodgm.ttf', 20)
        self.DRAW = True


    def draw(self):
        self.player.draw()
        if self.DRAW :
            self.image.clip_draw_to_origin(0, 0,223,352, *self.pos)
            pos1 = self.pos[0]+17, self.pos[1]
            self.select1.clip_draw_to_origin(0, 0,17,16, *self.spos)
            self.select2.clip_draw_to_origin(0, 0,17,16, *self.spos2)
            if self.stidx == 0:
                self.slist[0][0].clip_draw_to_origin(0, 0,31,31, 225,313)
                self.sname.draw(263,327,'정권',(255,255,255))
            elif self.stidx == 1:
                slist = ["호격권", "비기·맹호광파참"]
                for i in range(2): #나중에 스킬 유형별 개수 변수 추가하기
                    self.slist[0][0].clip_draw_to_origin(0, 0,31,31, 225,313 - i *32)
                    self.sname.draw(263,327 - i*32,slist[i],(255,255,255))
            elif self.stidx == 2:
                pass
            elif self.stidx == 3:
                slist = ["도주","방어"]
                for i in range(2):
                    self.slist[2][i].clip_draw_to_origin(0, 0,31,31, 225,313 - i *32)
                    self.sname.draw(263,327 - i*32,slist[i],(255,255,255))
        else :
            pass

    def update(self):

        
        x,y = self.spos
        x = self.spos[0]
        y = self.spos2[1]
        if self.stidx == 4:
            self.stidx = 0
        elif self.stidx == -1:
            self.stidx = 3

        if self.stidx == 0:
            self.st2idx = 0
        elif self.stidx == 1:
            if self.st2idx == 2:
                self.st2idx = 0
            elif self.st2idx == -1:
                self.st2idx = 1
        elif self.stidx == 2:
            self.st2idx = 0
        elif self.stidx == 3:
            if self.st2idx == 2:
                self.st2idx = 0
            elif self.st2idx == -1:
                self.st2idx = 1


        self.stidx = self.stidx % 4

        x = 217 + self.select1.w // 2 + self.stidx * 32
        y = 336 - self.select1.h - self.st2idx * 32

        self.spos = x, self.spos[1]
        self.spos2 =  self.spos2[0], y
        self.DRAW = self.player.update()

    def handle_event(self, e):
        self.player.handle_event(e)
        if e.type == SDL_KEYDOWN :
            self.stidx += \
                    -1 if e.key == SDLK_LEFT else \
                    1 if e.key == SDLK_RIGHT else 0
            self.st2idx += \
                    -1 if e.key == SDLK_DOWN else \
                    1 if e.key == SDLK_UP else 0
            if e.key == SDLK_SPACE :
                self.DRAW = False
                return self.stidx,self.st2idx
        return (-1,-1)

                    

    def get_bb(self):
    	pass