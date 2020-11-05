import random
import json
from pico2d import *
import gfw
from gobj import *


class MapObject():
    def __init__(self):
        self.mcount = 0
        self.x = []
        self.y = []
        self.width = []
        with open (res("object0.json")) as json_file:
            json_data = json.load(json_file)
            self.tile_list = json_data["data"]
            for i in range(len(self.tile_list)) :       
                if(self.tile_list[i] != 0):
                    self.x.append( ( ( i + 1) % 80 ) * 16 - 16) 
                    self.y.append( ( 59 - ( ( i + 1 ) // 80 ) ) * 16  + 128)
                    self.mcount += 1
                
        #print(self.mcount,self.x) # 59 - i
        
        self.delay = 0
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self,i):
        pos = self.x[i] ,self.y[i]
        x,y = self.bg.to_screen(pos)
        return x,y,x + 16,y + 16

    

