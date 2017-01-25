from random import uniform
from vec2d import *

class planet:
    
    #takes in position
    def __init__(self, p, image, moveList = None, angIncr = 0):
        self.pos = p #position
        if image:
            self.rect = image.get_rect()
            self.rect.center = p
        
        self.ang = 0
        self.angIncr = angIncr #angle of planet updated by this much every tick2
        if image:
            self.rad = image.get_rect().width/2 #radius
        
        self.image = image #surface used to render this planet
        
        self.moveList = moveList #used for meteors
        self.moveIndex = 0
        