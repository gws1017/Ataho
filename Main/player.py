import random
from pico2d import *
import gfw
import gobj
from random import randint

SKILL_NAME = ["tigerfist","lightslash"]

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
    KEYDOWN_SPACE  = (SDL_KEYDOWN, SDLK_SPACE)
    image = None

    #constructor
    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.battle = 0
        self.delta = 0, 0
        self.target = None
        self.speed = 200
        self.image = gfw.image.load(gobj.res('at_usual.png'))
        self.time = 0
        self.fidx = 0
        self.action = 2
        self.wbool = False
        self.mag = 1
        self.slevel = {
        SKILL_NAME[0]: [1,0],
        SKILL_NAME[1]: [1,0]
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
        self.name = gfw.font.load(gobj.RES_DIR + '/neodgm.ttf', 18)
            

        global center_x, center_y
        center_x = get_canvas_width() // 2
        center_y = get_canvas_height() // 2

    def set_target(self, target):
        x,y = self.pos
        tx,ty = target

        dx, dy = tx - x, ty - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0: return

        self.target = target
        self.delta = dx / distance, dy / distance
        self.action = 0 if dx < 0 else 1

    def draw(self):
        if self.target is not None:
            target = self.bg.to_screen(self.target)
            self.target_image.draw(*target)
        width,height = 48,64
        sx = self.fidx * width
        sy = self.action * height
        pos = self.bg.to_screen(self.pos)
        self.image.clip_draw(sx, sy, width, 64, *pos)

    def update(self):       
        
        x,y = self.pos
        tx,ty = self.pos
        px,py = self.pos
        dx,dy = self.delta
        x += dx * self.speed * self.mag * gfw.delta_time
        y += dy * self.speed * self.mag * gfw.delta_time

        bg_l, bg_b, bg_r, bg_t = self.bg.get_boundary()
        #print(self.bg.get_boundary())
        x = clamp(bg_l, x, bg_r)
        y = clamp(bg_b, y, bg_t)
        

        done = False
        if self.target is not None:
            tx,ty = self.target
            if dx > 0 and x >= tx or dx < 0 and x <= tx:
                x = tx
                done = True
            if dy > 0 and y >= ty or dy < 0 and y <= ty:
                y = ty
                done = True

        if done:
            self.target = None
            self.delta = 0, 0
            self.action = 2 if dx < 0 else 3

        
        if self.wbool :
            self.wcount += 1
    

        if self.battle == 0 :  
            self.pos = x,y
            if hasattr(self,'map_obj'):
                collides = gobj.collides_box(self,self.map_obj,0)
                if collides:
                    self.pos = px,py
 

        # self.bg.pos = 2 * center_x - x, 2 * center_y - y

        self.time += gfw.delta_time
        if self.delta[0] != 0 or self.delta[1] != 0:
            frame = self.time * 15
            self.fidx = int(frame) % 5
        else : self.fidx = 0

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            if self.battle == 1 :
                return
            else:
                if pair[1] == SDLK_DOWN or pair[1] == SDLK_UP or pair[1] == SDLK_LEFT or pair[1] == SDLK_RIGHT:    
                    if hasattr(self,'wcount') and pair[0] == SDL_KEYDOWN:
                        self.wbool = True
                if pair[1] == SDLK_DOWN and pair[1] == SDLK_UP and pair[1] == SDLK_LEFT and pair[1] == SDLK_RIGHT:
                    if pair[0] == SDL_KEYUP:
                        self.wbool = False
                        
                if self.target is not None:
                    self.target = None
                    self.delta = 0, 0
                pdx = self.delta[0]
                self.delta = gobj.point_add(self.delta, Player.KEY_MAP[pair])
                dx = self.delta[0]
                dy = self.delta[1]

                pd = self.action

                self.action = \
                    3 if dy < 0 else \
                    2 if dy > 0 else \
                    1 if dx < 0 else \
                    0 if dx > 0 else pd

    def get_bb(self):
        hw = 24
        hh = 32
        x,y = self.bg.to_screen(self.pos)
        return x -hw//2, y-hh, x + hw//2, y-hh//2

    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict['image']
        return dict

    def __setstate__(self, dict):
        # self.__init__()
        self.__dict__.update(dict)
        self.image = gfw.image.load(gobj.RES_DIR + '/at_usual.png')
