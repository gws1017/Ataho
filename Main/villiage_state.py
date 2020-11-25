import gfw
from pico2d import *
from gobj import *
from player import Player
from background import FixedBackground
from number import Number
from map_obj import MapObject
import life_gauge
import field_state
import setting

def enter(data):
    gfw.world.init(['bg','mobj','player', 'frame', 'status'])

    center = get_canvas_width() // 2, get_canvas_height() // 2
    bg = FixedBackground('Map0.png',0)
    gfw.world.add(gfw.layer.bg, bg)

    frame = FixedBackground('frame.png',1)
    gfw.world.add(gfw.layer.frame, frame)

    status = FixedBackground('statusui.png',2)
    status.tp = 2
    gfw.world.add(gfw.layer.status, status)

    global mobj
    mobj = MapObject(0)
    mobj.bg =bg
    gfw.world.add(gfw.layer.mobj,mobj)

    global number_w
    number_w = Number(3)

    global player
    if data == None :
        player = Player()
        player.pos = bg.center
    else : 
        player = data
    player.bg = bg
    if gfw.world.count_at(gfw.layer.mobj) > 0:
        player.map_obj = gfw.world.object(gfw.layer.mobj, 0)
    bg.target = player
    gfw.world.add(gfw.layer.player, player)

    global bgm,wav
    bgm = load_music('./res/bgm/villiage.MID')
    bgm.set_volume(50)
    bgm.repeat_play()
    wav = load_wav('./res/bgm/회복.WAV')

    life_gauge.load()


def update():
    gfw.world.update()
    x,y = player.bg.to_screen(player.pos)
    if x >= 20 and x <=50 :
        player.pos = 1200,236
        gfw.change_data(field_state,player)

def draw():
    gfw.world.draw()
    stat = player.STATUS
    player.name.draw(40,87,'아타호',(255,255,255))
    mobj.name.draw(528,87,'마을',(255,255,255))
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
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            bgm.stop()
            gfw.push_data(setting,player)
            return
        if e.key == SDLK_SPACE:
            x,y = player.pos
            if x >= 625 and x <= 685:
                if y >= 555 and y<= 610:
                    player.STATUS["curHp"] = player.STATUS["maxHp"]
                    player.STATUS["curMp"] = player.STATUS["maxMp"]
                    wav.play(1)

    if player.handle_event(e):
        return
def pause():
    pass

def exit():
    gfw.world.clear()


if __name__ == '__main__':
    gfw.run_main()
