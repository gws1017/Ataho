from pico2d import *
from gobj import *
import gfw_image

RES_DIR = '../res'

class Ball:
    balls = []
    def __init__(self, pos, delta, big=False): 
        imageName = '/ball41x41.png' if big else '/ball21x21.png' #큰공(부울변수)이라면 큰공이미지 아니라면 작은 이미지 
        self.image = gfw_image.load(RES_DIR + imageName) #이미지는 각자 다같고있지만 가리키는 이미지는 하나이다.(gfw_image에서 저장된걸
        self.pos = pos                                   #불러온다)
        self.delta = delta
        self.radius = self.image.h // 2
        # print('Radius = %d' % self.radius)
    def draw(self):
        self.image.draw(*self.pos)
    def update(self):
        x,y = self.pos
        dx,dy = self.delta
        x += dx
        y += dy
        gravity = 0.1
        dy -= gravity

        bottom = y - self.radius
        if bottom < 50 and dy < 0: #바닥 보다 작거나 아래로 떨어지고있다면
            dy *= rand(-0.8) #에너지 손실 90~110퍼사이 
            if dy <= 1: # 튀는양이 어느정도 했으면 고만 튀자
                dy = 0

        if x < -100 or x > get_canvas_width() + 100: # 실제 캔버스크기보다 조금 큰 사이즈에서 벗어난경우 삭제하는 것이 좋다
            Ball.balls.remove(self)
            print('Ball count - %d' % len(Ball.balls))

        self.pos = x, y
        self.delta = dx, dy
    