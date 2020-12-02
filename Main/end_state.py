import gfw
import gobj
from number import Number
from player import Player
from pico2d import *
canvas_width = 640
canvas_height = 480

Dan = {
  (40)  : "단외 보통호랑이",
  (60)  : "1단 보통권사",
  (80)  : "2단 난폭권사",
  (100)  : "3단 강권사",
  (120)  : "4단 유명권사",
  (140)  : "5단 사범대리",
  (160)  : "6단 사범",
  (180)  : "7단 권호",
  (200)  : "8단 권제",
  (210)  : "9단 권황",
  (220)  : "10단 지고의 권사",
  (260)  : "11단 권성",
  (270)  : "12단 권신",
  (280)  : "13단 전설의 맹호",
}

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
    font.draw(100,327+25,'플레이어 레벨  :' ,(255,255,255))
    number_w.draw(360,327+25,st["lvl"],1)
    font.draw(100,302+25,'플레이어 공격력:' ,(255,255,255))
    number_w.draw(360,302+25,st["atk"],1)
    font.draw(100,277+25,'플레이어 방어력:' ,(255,255,255))
    number_w.draw(360,277+25,st["df"],1)
    font.draw(100,252+25,'호격권 레벨    :' ,(255,255,255))
    number_w.draw(360,252+25,sl["tigerfist"][0],1)
    font.draw(100,227+25,'맹호광파참 레벨:' ,(255,255,255))
    number_w.draw(360,227+25,sl["lightslash"][0],1)

    font.draw(100,202+25,'총 점수: ' ,(255,255,255))
    sumslvl = sl["lightslash"][0]+sl["tigerfist"][0]
    sumlvl = st["lvl"]
    sums = sumslvl*10 + sumlvl*20
    number_w.draw(360,202+25,sums,1)

    if sums == 50 : sums = 60
    elif sums == 70 or sums == 90 or sums == 110 or sums == 130 or sums == 150 or sums == 170 or sums == 190 : sums += 10  
    elif sums >= 230 and sums <= 250 : sums = 220

    font.draw(100,177+25,'단수 : ' ,(255,255,255))
    if sums >= 280 : sums = 280
    font.draw(200,177+25,Dan[sums] ,(255,255,255))
    if sums == 40 : font.draw(100,152+25,'최하위 단수네요 이 점수 나오기도 힘든데?' ,(255,255,255))

    font2.draw(10,100,'원작이 더 재밌어요' ,(255,255,255))
    font2.draw(150,30,'원작하세요' ,(255,255,255))
    

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
def exit():
    global image,bgm
    bgm.stop()
    del image
    del bgm

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
   gfw.run_main()

