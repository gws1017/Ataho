import gfw
from pico2d import *
from gobj import *
from player import Player
from background import FixedBackground
from number import Number
from map_obj import MapObject
import life_gauge

def enter():
    gfw.world.init(['bg','mobj','player', 'frame', 'status'])

    center = get_canvas_width() // 2, get_canvas_height() // 2
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
    player = Player()
    player.pos = bg.center
    player.bg = bg
    bg.target = player
    gfw.world.add(gfw.layer.player, player)

    global bgm
    bgm = load_music('./res/bgm/field.MID')
    bgm.set_volume(50)
    bgm.repeat_play()

    #global nm
    #nm = gfw.font.load(gobj.RES_DIR + '/neodgm.ttf', 20)

    life_gauge.load()


def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    player.name.draw(40,87,'아타호',(255,255,255))
    mobj.name.draw(528,87,'황야1',(255,255,255))
    life_gauge.draw(174,84,player.curHp / player.maxHp)
    number_w.draw(212,98,player.curHp,0.65)
    number_w.draw(262,98,player.maxHp,0.65)
    life_gauge.draw(272,84,player.curMp / player.maxMp)
    number_w.draw(310,98,player.curMp,0.65)
    number_w.draw(360,98,player.maxMp,0.65)
    life_gauge.draw(370,84,player.curExp / player.maxExp)
    number_w.draw(408,98,player.curExp,0.65)
    number_w.draw(465,98,player.maxExp,0.65)
    draw_collision_box()
    # gobj.draw_collision_box()

def handle_event(e):
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
            return

    if player.handle_event(e):
        return

def exit():
    pass



if __name__ == '__main__':
    gfw.run_main()
