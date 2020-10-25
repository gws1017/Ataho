import time
from pico2d import *

running = True
stack = None
frame_interval = 0.01
delta_time = 0

objects = []
trashcan = []

def init(layer_names):
    global objects
    objects = []
    gfw.layer = lambda: None
    layerIndex = 0
    for name in layer_names:
        objects.append([])
        gfw.layer.__dict__[name] = layerIndex
        layerIndex += 1
        
def quit():
    global running
    running = False

def run(start_state):
    global running, stack
    running = True
    stack = [start_state]

    w ,h = 640,480

    if hasattr(start_state, 'canvas_width'): w = start_state.canvas_width 
    if hasattr(start_state, 'canvas_height'): h = start_state.canvas_height

    open_canvas(w = w, h = h)

    start_state.enter()

    global delta_time
    last_time = time.time() #시작시간 기록
    while running:
        
        now = time.time() #현재시간 계속 기록
        delta_time = now - last_time #지속시간 저장
        last_time = now # 초기화

        # 이벤트 관리
        evts = get_events()
        for e in evts:
            stack[-1].handle_event(e)

        # game logic
        stack[-1].update()

        # game rendering
        clear_canvas()
        stack[-1].draw() #맨위에 있는거 (-1)
        update_canvas()

        delay(frame_interval)

    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

    close_canvas()

def change(state):
    global stack
    if (len(stack) > 0):
        stack.pop().exit()
    stack.append(state) #리스트에 스테이트 추가
    state.enter()

def push(state):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()

def pop():
    global stack
    size = len(stack)
    if size == 1:
        quit()
    elif size > 1:
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

        # execute resume function of the previous state
        stack[-1].resume()

def run_main():
    import sys
    main_module = sys.modules['__main__']
    run(main_module)
