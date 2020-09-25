from pico2d import *

from random import *

from gobj import Grass, Boy

def handle_events():
    global running
    global boy

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                boy.dx += 1
                boy.dx2 = 1
            elif event.key == SDLK_LEFT:
                boy.dx -= 1
                boy.dx2 = -1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                boy.dx -= 1
                boy.image.clip_draw(0, 300 ,100, 100, boy.x, 90)
            elif event.key == SDLK_LEFT:
                boy.dx += 1
                boy.image.clip_draw(0, 200 ,100, 100, boy.x, 90)
        elif event.type == SDL_MOUSEMOTION:
            boy.x, boy.y = event.x, get_canvas_height() - event.y - 1



open_canvas()

team = [Boy() for i in range(11)]

boy = team[0]
boy.dx = 0

grass = Grass()

running = True


hide_cursor()

while running:
    clear_canvas()
    
    grass.draw()

    for b in team : b.draw()
    
    update_canvas()
    handle_events()
    
    for b in team: b.update()

    delay(0.03)

close_canvas()
