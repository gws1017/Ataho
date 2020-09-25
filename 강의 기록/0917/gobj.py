from random import *

from pico2d import *

class Boy:
    def __init__(self):
        self.x, self.y = randint(100,700),randint(100,500)
        self.image = load_image('../image/animation_sheet.png')
        self.dx, self.dx2 = 1,1 #dx2 는 보이가 멈췄을때 이미지 방향을 잡아주기
        self.f = randint(0,7)   #위한 변수입니다
    def draw(self):
         if self.dx == 1:
            self.image.clip_draw(self.f * 100, 100 ,100, 100, self.x, self.y)
         elif self.dx == -1:
            self.image.clip_draw(self.f * 100, 0 ,100, 100, self.x, self.y)
         elif self.dx == 0:
             if self.dx2 == 1:
                self.image.clip_draw(self.f * 100, 100 ,100, 100, self.x, self.y)
             elif self.dx2 == -1:
                self.image.clip_draw(self.f * 100, 0 ,100, 100, self.x, self.y)
    def update(self):
        self.f = (self.f + 1) % 8
        self.x += self.dx * 5

class Grass:
    def __init__(self):
        self.x , self.y = 400, 30
        self.img = load_image('../image/grass.png')
    def draw(self):
        self.img.draw(self.x,self.y)
