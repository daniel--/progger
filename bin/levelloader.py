from planet import planet
from vec2d import vec2d
from level import level
import pygame
from random import uniform

class planet2:
    
    def __init__(self,point,rad,rot):
        self.pos  = point
        self.rad = rad
        self.rot = rot
        self.ang = 0
        self.goal = -1

class levelLoader:
    
    def __init__(self):
        self.images=[]
        for i in range(1, 9):
            self.images.append(pygame.image.load(\
                        'planets/planet_' + `i` + '.png'))
        
        self.earthImg = pygame.image.load('planets/earth.png')
    def loadLevel(self,name,editor = 0):
        file = open(name,'r')
        planetstring = file.readline()
        line = file.readline()
        #print '#',line,'#'
        goali,goal = eval(line)
        sp = eval(file.readline())
        if not editor:
            sp = vec2d(sp[0],sp[1])
        planets = eval(planetstring)
        realplanets = []
        for p in planets:
            pos,rad,i,rot = p
            if editor:
                plan = planet2(vec2d(pos),rad,rot)
                plan.imageIndex = i
                realplanets.append(plan)
            else:
                s = int(2 * rad / 0.96) #magic
                if i == 100:
                    tempi = pygame.transform.scale(self.earthImg, (s,s))
                else:
                    tempi = pygame.transform.scale(self.images[i],(s,s))
                v = vec2d(pos[0],pos[1])
                realplanets.append(planet(v,tempi,angIncr = rot))
        paths = eval(file.readline())
        meteors = []
        if editor:
            meteors = paths
        else:
            mimage = pygame.image.load('potato2.png')
            for p in paths:
                m = planet(p[0],mimage,moveList = p,angIncr = uniform(3,6))
                meteors.append(m)
        l = level(realplanets,sp,meteors)
        if editor:
            realplanets[goali].goal = goal
        else:
            l.goalPlanet = realplanets[goali]
            l.goalAngle = goal
        return l
