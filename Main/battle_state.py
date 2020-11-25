import gfw
from pico2d import *
from gobj import *
from background import Battleground
from background import FixedBackground
from number import Number
from map_obj import MapObject
from random import randint
from battle_manage import BattleManager
import end_state
import field_state
import field_state2
import life_gauge
import gobj

# 맵정보를 딕셔너리로 저장

def enter(data,tp,bt):
    gfw.world.init(['bg','frame', 'status'])

    center = get_canvas_width() // 2, get_canvas_height() // 2
    bg = Battleground('battle0.png',0)
    gfw.world.add(gfw.layer.bg, bg)

    frame = FixedBackground('frame.png',1)
    gfw.world.add(gfw.layer.frame, frame)

    status = FixedBackground('bt_statusui.png',2)
    status.tp = 2
    gfw.world.add(gfw.layer.status, status)

    global Map
    Map = tp

    global p
    p = data

    global bm
    bm = BattleManager(bt,tp)
    bm.player.bgm2 = load_music('./res/bgm/victory.MID')
    bm.player.STATUS = p.STATUS
    bm.player.slevel = p.slevel
    bm.oplayer = data

    global number_w
    number_w = Number(3)   

    global bgm
    if bt == 0:
        if tp == 0:
            bgm = load_music('./res/bgm/battle0.MID')
        if tp == 1:
            bgm = load_music('./res/bgm/battle1.MID')
    elif bt == 1:
        bgm = load_music('./res/bgm/보스1.MID')
    bgm.set_volume(50)
    bgm.repeat_play()
    
    global ft
    ft = gfw.font.load(RES_DIR + '/neodgm.ttf', 18)

    life_gauge.load()



def update():
    gfw.world.update()
    isreturn = bm.update()
    if isreturn == -1 :
        if bm.player.STATUS["curHp"] == 0 : bm.player.STATUS["curHp"] = 1 
        bm.oplayer.STATUS = bm.player.STATUS
        if bm.player.slevel['tigerfist'][1] >=10 :
            bm.player.slevel['tigerfist'][1] = 0
            bm.player.slevel['tigerfist'][0] += 1
        if bm.player.slevel['lightslash'][1] >=10 :
            bm.player.slevel['lightslash'][1] = 0
            bm.player.slevel['lightslash'][0] += 1
        print(bm.player.slevel['lightslash'][0],bm.player.slevel['lightslash'][1])
        bm.oplayer.slevel = bm.player.slevel
        print(bm.oplayer.slevel['lightslash'][0],bm.oplayer.slevel['lightslash'][1])
        bm.oplayer.wcount = 0
        bm.oplayer.wmax = randint(50,80)
        bm.oplayer.delta = 0,0 
        if Map == 0:  
            gfw.change_data(field_state,bm.oplayer)
        elif Map == 1:
            gfw.change_data(field_state2,bm.oplayer)
    elif isreturn == -3 :
            gfw.change_data(end_state,bm.oplayer)

def draw():
    p = bm.player
    m = bm.monster

    st = p.STATUS
    st2 = m.STATUS
    
    gfw.world.draw()
    bm.draw()

    ft.draw(40,87,p.name,(255,255,255))
    life_gauge.draw(174,84,st["curHp"] / st["maxHp"])
    number_w.draw(212,98,st["curHp"],0.65)
    number_w.draw(262,98,st["maxHp"],0.65)
    life_gauge.draw(272,84,st["curMp"] / st["maxMp"])
    number_w.draw(310,98,st["curMp"],0.65)
    number_w.draw(360,98,st["maxMp"],0.65)
    life_gauge.draw(370,84,st["curExp"] / st["maxExp"])
    number_w.draw(408,98,st["curExp"],0.65)
    number_w.draw(465,98,st["maxExp"],0.65)

    
    ft.draw(480,94,m.name,(255,255,255))
    life_gauge.draw(541,90,st2["curHp"] / st2["maxHp"])
    number_w.draw(587,105,st2["curHp"],0.65)
    number_w.draw(630,105,st2["maxHp"],0.65)

def handle_event(e):
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
            return

    if bm.handle_event(e):
        return
def pause():
    pass
def exit():
    gfw.world.clear()



if __name__ == '__main__':
    gfw.run_main()
