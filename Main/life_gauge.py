from pico2d import *
import gfw
import gobj

def load():
    global bg, fg
    #bg = gfw.image.load(gobj.RES_DIR + '/gauge_bg.png')
    fg = gfw.image.load(gobj.RES_DIR + '/gauge_fg.png')

def draw(x, y,rate):
    l = x - fg.w // 2
    b = y - fg.h // 2
    #draw_3(bg, l, b, width, 3)
    draw_3(fg, x, y, round(fg.w * rate))

def draw_3(img, l, b, width):
    img.clip_draw_to_origin(0, 0, img.w, img.h, l, b, width, img.h)

