from pico2d import *

def handle_events():
    global running
    global x, y
    global dx, dx2
#dx2 는 멈춰 서있을 때 이미지를 그려주기위해 추가한 변수
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dx += 1
                dx2 = 1
            elif event.key == SDLK_LEFT:
                dx -= 1
                dx2 = -1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dx -= 1
                character.clip_draw(0, 300 ,100, 100, x, 90)
            elif event.key == SDLK_LEFT:
                dx += 1
                character.clip_draw(0, 200 ,100, 100, x, 90)
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, get_canvas_height() - event.y - 1

open_canvas()
grass = load_image('../image/grass.png')
character = load_image('../image/animation_sheet.png')

running = True

x = 400
y = 90
frame = 0
dx = 0
dx2 = 1

hide_cursor()

while running:
    clear_canvas()
    grass.draw(400,30)
    
    if dx == 1:
        character.clip_draw(frame * 100, 100 ,100, 100, x, y)
    elif dx == -1:
        character.clip_draw(frame * 100, 0 ,100, 100, x, y)
    elif dx == 0:
        if dx2 == 1:
            character.clip_draw(0, 300 ,100, 100, x, y)
        elif dx2 == -1:
            character.clip_draw(0, 200 ,100, 100, x, y)
    

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    x += dx * 5
    delay(0.03)

close_canvas()
