import random
import json
from pico2d import *
import gfw
from gobj import *


class JsonObject():
    def __init__(self):
        self.count = 0
        self.x = []
        self.y = []
        with open (res("object0.json")) as json_file:
            json_data = json.load(json_file)

            self.tile_list = json_data["data"]
            for i in range(len(self.tile_list)) :
                if(self.tile_list[i] != 0):
                    self.count += 1
                    self.x.append((i % 80)*16) 
                    self.y.append((59 - (i // 80))*16)



        #print(self.tile_list[4],self.count,self.x) # 59 - i
        
        self.delay = 0
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self,i):
        pos = self.x[i] ,self.y[i]
        
        return *pos,pos[0] + 16,pos[1] + 16

    
        
