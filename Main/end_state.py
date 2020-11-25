import gfw
import gobj
from number import Number
from pico2d import *
canvas_width = 640
canvas_height = 480

def enter(data):
   global image, bgm
   image = load_image('./res/ed.png')
   bgm = load_music('./res/bgm/end.MID')
   bgm.set_volume(50)
   bgm.repeat_play()

   global player
   player = data

   global font ,font2
   font = gfw.font.load (gobj.RES_DIR + '/neodgm.ttf', 25)
   font2 = gfw.font.load (gobj.RES_DIR + '/neodgm.ttf', 70)

   global number_w
   number_w = Number(3) 



def update():
    pass

def draw():
    global image, font
    st = player.STATUS
    sl = player.slevel
    image.draw(canvas_width//2,canvas_height//2)#한 가운데 중심으로 그려줌
    font2.draw(210,400,'THE END' ,(255,255,255))
    font.draw(100,327,'플레이어 레벨  :' ,(255,255,255))
    number_w.draw(340,327,st["lvl"],1)
    font.draw(100,302,'플레이어 공격력:' ,(255,255,255))
    number_w.draw(340,302,st["atk"],1)
    font.draw(100,277,'플레이어 방어력:' ,(255,255,255))
    number_w.draw(340,277,st["df"],1)
    font.draw(100,252,'호격권 레벨    :' ,(255,255,255))
    number_w.draw(340,252,sl["tigerfist"][0],1)
    font.draw(100,227,'맹호광파참 레벨:' ,(255,255,255))
    number_w.draw(340,227,sl["lightslash"][0],1)
    font2.draw(10,100,'원작이 더 재밌어요' ,(255,255,255))
    font2.draw(150,30,'원작하세요' ,(255,255,255))
    

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
def exit():
    global image
    bgm.stop()
    del image

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
   gfw.run_main()

