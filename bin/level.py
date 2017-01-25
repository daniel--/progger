from planet import *
from vec2d import *
import pygame

images=[]
for i in range(1, 9):
    images.append(pygame.image.load('planets/planet_' + `i` + '.png'))

class level:
    
    def __init__(self,p,s,m):
        self.p = p
        self.s = s
        self.m = m
        self.pm = self.p + self.m
        self.goalPlanet = self.p[0]
        self.goalAngle = 0
        