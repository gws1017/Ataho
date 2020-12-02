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
import villiage_state
import field_state
import field_state2
import life_gauge
import gobj

# 맵정보를 딕셔너리로 저장

def enter(data,bt,tp):
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
    bm.player.PLAYER_SINFO = p.PLAYER_SINFO
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

    global die_time,flag_die
    die_time = 0
    flag_die = False

def final_up():
    if bm.player.STATUS["curHp"] == 0 : bm.player.STATUS["curHp"] = 1 
    bm.player.PLAYER_SINFO = {
          (0,0) :  bm.player.STATUS["atk"],
          (1,0) :  bm.player.STATUS["atk"]*(bm.player.slevel["tigerfist"][0]*0.1+1),
          (1,1) :  bm.player.STATUS["atk"]*(bm.player.slevel["lightslash"][0]*0.1+1)*1.2,
          (2,0) : 0,
          (3,0) : 0,
          (3,1) : 0
        }
    bm.oplayer.STATUS = bm.player.STATUS
    bm.oplayer.PLAYER_SINFO = bm.player.PLAYER_SINFO

    if bm.player.slevel['tigerfist'][1] >=10 :
        bm.player.slevel['tigerfist'][1] = 0
        bm.player.slevel['tigerfist'][0] += 1
    if bm.player.slevel['lightslash'][1] >=10 :
        bm.player.slevel['lightslash'][1] = 0
        bm.player.slevel['lightslash'][0] += 1
    bm.oplayer.slevel = bm.player.slevel
    bm.oplayer.delta = 0,0
    bm.oplayer.wcount = 0
    bm.oplayer.wmax = randint(50,80)

def update():
    global die_time,flag_die
    gfw.world.update()
    isreturn = 0
    if flag_die == False:
        isreturn = bm.update()
    else:
        bm.player.update()
        die_time += gfw.delta_time
        if die_time > 3:
            final_up()
            if bm.BE == 1 :
                bm.oplayer.pos = 320,240
                gfw.change_data(villiage_state,bm.oplayer)
            else :
                if Map == 0: 
                    gfw.change_data(field_state,bm.oplayer)
                elif Map == 1:
                    gfw.change_data(field_state2,bm.oplayer)
    if isreturn == -1 :
        final_up()
        if Map == 0:  
            gfw.change_data(field_state,bm.oplayer)
        elif Map == 1:
            gfw.change_data(field_state2,bm.oplayer)
    elif isreturn == -3 :
        gfw.change_data(end_state,bm.oplayer)
    elif isreturn == -10:
        flag_die = True




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
    if bm.handle_event(e):
        pass
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
            return

   
def pause():
    pass
def exit():
    global bgm
    del bgm
    gfw.world.clear()



if __name__ == '__main__':
    gfw.run_main()
