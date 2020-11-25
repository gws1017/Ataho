import gfw
from pico2d import *
import villiage_state
import field_state2
import field_state
import pickle
from player import * 
canvas_width = 640
canvas_height = 480

def enter(data):
   global image, selector
   image = load_image('./res/setting.png')
   selector = load_image('./res/select2.png')

   global st_num
   st_num = 0

   global player
   player = data


   global wav
   wav = load_wav('./res/bgm/선택.WAV')
   


def update():
    global st_num

    if st_num <= -1 : st_num = 1
    elif st_num >= 2 : st_num = 0
    
def draw():
    global image,selector,st_num
    image.draw(canvas_width//2,canvas_height//2)#한 가운데 중심으로 그려줌
    selector.draw(110+st_num*150,200,64,64)

def handle_event(e):  
    global st_num

    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            st_num -= 1
            wav.set_volume(50)
            wav.play(1)
        elif e.key == SDLK_RIGHT:
            st_num += 1
            wav.set_volume(50)
            wav.play(1)
        elif e.key == SDLK_SPACE:
            if st_num == 1:
                gfw.change_data(villiage_state,player)
            elif st_num == 0:
                save()
                gfw.change_data(villiage_state,player)


def exit():
    global image
    del image

def save():
    data = player.__getstate__()
    with open('save.sav','wb') as f:
        pickle.dump(data,f)

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
   gfw.run_main()

