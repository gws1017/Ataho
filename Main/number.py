from pico2d import *
import gfw
from gobj import *

class Number:
    def __init__(self, h): # h 0 빨강 1 노랑 2 초록 3 흰색
        # self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.image = gfw.image.load(RES_DIR + '/num.png')
        self.digit_width = self.image.w // 10
        self.digit_height = self.image.h // 4
        self.nidx = h
        self.reset()

    def reset(self):
        self.score = 0
        self.display = 0

    def draw(self,right,y,point,size):
        x = right
        number = point
        while number > 0:
            digit = number % 10

            sx = digit * self.digit_width
            sy = self.digit_height * self.nidx
            dx = self.digit_width * size
            dy = self.digit_height * size

            # print(type(sx), type(digit), type(self.digit_width))
            x -= self.digit_width * size
            self.image.clip_draw(sx, sy, self.digit_width, self.digit_height, x, y, dx,dy)
            number //= 10
        if point == 0 :
            sy = self.digit_height * self.nidx
            dx = self.digit_width * size
            dy = self.digit_height * size
            self.image.clip_draw(0, sy, self.digit_width, self.digit_height, x, y, dx,dy)

    def update(self):
        pass
