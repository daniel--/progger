from vec2d import *

class frog:
    def __init__(self, pos, image):
        self.pos = pos
        
        self.rect = image.get_rect()
        self.rect.center = pos
        
        self.ang = 0 #angle for drawing
        self.tang = 0 #target angle
        self.angIncr = 25 #increment of angle
        
        self.oldpos = vec2d(pos.x,pos.y)
        self.acc = vec2d(0,0)
        self.image = image
        self.planet = None #planet the frog is landed on

        self.jumpStart = 0 #timestamp of when the jump started
        self.jumping = False #is frog in process of jumping?
        self.jumpStrength = 0 #force of jump
        self.jumpThisFrame = False #O.M.F.G.
        
class tongue:
    def __init__(self):
        self.pos = None
        self.vel = None #None if the tongue is not used, a vec2d if it is
        
        self.latched = None #stores pointer to the meteor if latched
        self.dist = 0
        self.k = 0.007 #how strong it is
        
        