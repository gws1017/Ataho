from pico2d import *

images = {} #딕셔너리

def load(file): #캐시의 원리 로드해놓은 이미지가 있으면
    global images
    if file in images:
        return images[file] #저장된것을 재활용

    image = load_image(file) #없으면 새로 불러온다
    images[file] = image
    return image

def unload(file):
    global images
    if file in images:
        del images[file]
