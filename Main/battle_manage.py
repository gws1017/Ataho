import gfw
import gobj
from pico2d import *

class BattleManager:
    def __init__(self):
        self.image = gfw.image.load(gobj.res('skillwindow.png'))
        self.select1 = gfw.image.load(gobj.res('select1.png'))
        self.slist = [[gfw.image.load(gobj.res('skill1.png'))],
                      [],
                      [gfw.image.load(gobj.res('run.png')),gfw.image.load(gobj.res('defense.png'))] ]

        self.pos = 200,128
        self.spos = 217 + self.select1.w // 2,409 - self.select1.h
        self.stidx = 0
        self.sname = gfw.font.load(gobj.RES_DIR + '/neodgm.ttf', 18)


    def draw(self):
        self.image.clip_draw_to_origin(0, 0,223,352, *self.pos)
        pos1 = self.pos[0]+17, self.pos[1]
        self.select1.clip_draw_to_origin(0, 0,17,16, *self.spos)

        if self.stidx == 0:
            self.slist[0][0].clip_draw_to_origin(0, 0,31,31, 225,313)
            self.sname.draw(256,313,'정권'(255,255,255))
        elif self.stidx == 1:
            for i in range(2):
                self.slist[0][0].clip_draw_to_origin(0, 0,31,31, 225,313 - i *32)
        elif self.stidx == 2:
            pass
        elif self.stidx == 3:
            for i in range(2):
                self.slist[2][i].clip_draw_to_origin(0, 0,31,31, 225,313 - i *32)

    def update(self):
        x,y = self.spos

        if self.stidx == 4:
            self.stidx = 0
        elif self.stidx == -1:
            self.stidx = 3

        self.stidx = self.stidx % 4

        x = 217 + self.select1.w // 2 + self.stidx * 32
        print(self.stidx)

        self.spos = x,y

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN :
            self.stidx += \
                    -1 if e.key == SDLK_LEFT else \
                    1 if e.key == SDLK_RIGHT else 0
                    

    def get_bb(self):
    	pass