import gfw
import pickle
from pico2d import *
import villiage_state
import field_state2
from player import Player
canvas_width = 640
canvas_height = 480

def enter():
   global image, bgm
   image = load_image('./res/title.png')
   bgm = load_music('./res/bgm/main.MID')
   bgm.set_volume(50)
   bgm.repeat_play()


def update():
    pass

def draw():
    global image
    image.draw(canvas_width//2,canvas_height//2)#한 가운데 중심으로 그려줌
    

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
        load()
        if data == None:
          gfw.change_data(villiage_state,None)
        else :
          gfw.change_data(villiage_state,player)

def exit():
    global image
    bgm.stop()
    del image

def load():
    global data, player
    data = None
    try:
        f = open('save.sav', "rb")
        data = pickle.load(f)
        f.close()
        player = Player()
        player.__setstate__(data)
    except:
        print("No highscore file")
        data = None
        return
 
    
def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
   gfw.run_main()

