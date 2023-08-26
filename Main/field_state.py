import gfw
from pico2d import *
from gobj import *
from player import Player
from background import FixedBackground
from number import Number
from map_obj import MapObject
from random import randint
import life_gauge
import villiage_state
import battle_state
import field_state2

def enter(data = None):
    gfw.world.init(['bg','mobj','player', 'frame', 'status'])

    center = get_canvas_width() // 2, get_canvas_height() // 2
    global bg
    bg = FixedBackground('Map1.png',0)
    gfw.world.add(gfw.layer.bg, bg)

    frame = FixedBackground('frame.png',1)
    gfw.world.add(gfw.layer.frame, frame)

    status = FixedBackground('statusui.png',2)
    status.tp = 2
    gfw.world.add(gfw.layer.status, status)

    global mobj
    mobj = MapObject(1)
    mobj.bg = bg
    gfw.world.add(gfw.layer.mobj,mobj)

    global number_w
    number_w = Number(3)

    global player
    if data != None :
        player = data
    else : 
        player = Player()
    player.bg = bg
    player.wcount = 0
    player.wbool = False
    player.wmax = randint(50,80)

    if(data == None) :
        x,y = player.pos
        y +=50
        player.pos = x,y
    
    if gfw.world.count_at(gfw.layer.mobj) > 0:
        player.map_obj = gfw.world.object(gfw.layer.mobj, 0)
    bg.target = player
    gfw.world.add(gfw.layer.player, player)

    global bgm
    bgm = load_music('./res/bgm/field.MID')
    bgm.set_volume(50)
    bgm.repeat_play()


    life_gauge.load()


def update():
    if hasattr(player,'wcount'):
        if player.wcount > player.wmax :
            player.wcount = 0
            gfw.change_bt(battle_state,player,0,0)

    gfw.world.update()
    x,y = player.pos
    if x >= 1220 and x<=1260 :
        player.pos = 80,236
        gfw.change_data(villiage_state,player)
    if y >= 1050 :#and player.STATUS["lvl"] >= 10:
        player.pos = 264,213
        gfw.change_data(field_state2,player)
        

def draw():
    gfw.world.draw()
    stat = player.STATUS
    player.name.draw(40,87,'아타호',(255,255,255))
    mobj.name.draw(528,87,'황야1',(255,255,255))
    life_gauge.draw(174,84,stat["curHp"] / stat["maxHp"])
    number_w.draw(212,98,stat["curHp"],0.65)
    number_w.draw(262,98,stat["maxHp"],0.65)
    life_gauge.draw(272,84,stat["curMp"] / stat["maxMp"])
    number_w.draw(310,98,stat["curMp"],0.65)
    number_w.draw(360,98,stat["maxMp"],0.65)
    life_gauge.draw(370,84,stat["curExp"] / stat["maxExp"])
    number_w.draw(408,98,stat["curExp"],0.65)
    number_w.draw(465,98,stat["maxExp"],0.65)

def handle_event(e):
    if player.handle_event(e):
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
    bgm.stop()
    del bgm
    gfw.world.clear()



if __name__ == '__main__':
    gfw.run_main()
