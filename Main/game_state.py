import gfw
from pico2d import *
from title_state import *
from player import Player
canvas_width = 640 
canvas_height = 480


def enter():
    global image, bgm
    image = load_image('../res/Map0.png')
    #bgm = load_music('../res/bgm/villiage.MID')
    #bgm.set_volume(50)
    #bgm.repeat_play()

    global player
    player = Player()
    player.pos = (320,80)


def update():
    player.update()
    pass

def draw():
    global image

    

    x,y = (player.pos[0]*2, player.pos[1]*2)
   
   

    if x < 0 :
        x = 0 
    elif x > 640 :
        x = 640
    if y < 0 :
        y = 0
    elif y > 480 :
        y = 480

    #print(x,y) 
    image.clip_draw(int(x),int(y),640,480,canvas_width//2,canvas_height//2)
    player.draw()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
        gfw.push(game_state)
    if player.handle_event(e):
        return
def exit():
    global image,bgm
    del image,bgm

def pause():
    pass
def resume():
    pass
    
if __name__ == '__main__':
    gfw.run_main()