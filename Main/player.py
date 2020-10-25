import random
from pico2d import *
import gfw
import gobj


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
        self.delta = 0, 0
        self.target = None
        self.speed = 300
        self.image = load_image('../res/at_usual.png')
        self.time = 0
        self.fidx = 0
        self.action = 0
        self.mag = 1
        self.pd = 0


    #def set_target(self, target):
    #    x,y = self.pos
    #    tx,ty = target
    #    dx, dy = tx - x, ty - y
    #    distance = math.sqrt(dx**2 + dy**2)
    #    if distance == 0: return

    #    self.target = target
    #    self.delta = dx / distance, dy / distance
    #    self.action = 0 if dx < 0 else 1

    def draw(self):
        width,height = 48,64
        sx = self.fidx * width
        sy = self.action * height


        self.image.clip_draw(sx, sy, 48, 64, self.pos[0],self.pos[1]) 
        #if self.pos[1] - 240 > 0:
        #    self.image.clip_draw(sx, sy, width, 64, self.pos[0],240)
        #else :
        #    self.image.clip_draw(sx, sy, width, 64, self.pos[0],self.pos[1]) 
        
    def update(self):
        x,y = self.pos
        dx,dy = self.delta
        
        x += (dx * self.speed * self.mag * gfw.delta_time)/2
        y += (dy * self.speed * self.mag * gfw.delta_time)/2
        if x < 10:
            x = 10
        if y < 10 :
            y = 10
        if x > 630:
            x = 630
        if y > 470 :
            y = 470

        done = False
        
        self.pos = x,y

        self.time += gfw.delta_time
        
        if self.delta[0] != 0 or self.delta[1] != 0:
            frame = self.time * 15
            self.fidx = int(frame) % 5
        else : self.fidx = 0

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
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
            print ( self.pos)
            # print(dx, pdx, self.action)
        

    def get_bb(self):
        hw = 20
        hh = 40
        x,y = self.pos
        return x - hw, y - hh, x + hw, y + hh
