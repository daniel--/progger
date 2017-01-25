import pygame
from pygame.locals import *
from vec2d import *
import sys
from levelloader import levelLoader
import os

class planet:
    
    def __init__(self,point,rad,rot):
        self.pos  = point
        self.rad = rad
        self.rot = rot
        self.ang = 0
        self.goal = -1

def drawFont( text, color = (255,255,255), font = 'courier', size = 18):
		fontObj = pygame.font.SysFont(font, size)
		return fontObj.render(text, True, color)

class levelEditor:
    """The level editor"""
    
    def __init__(self,file):
        self.file = file
        self.w = 1024
        self.h = 768
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill((0,0,0))
        
        self.images=[]
        for i in range(1, 9):
            self.images.append(pygame.image.load(\
                        'planets/planet_' + `i` + '.png'))
        
        self.currentImage = 0
        
        self.initialPoint = vec2d(0,0)
        self.finalPoint = vec2d(0,0)
        
        self.movep = None
        
        self.startPoint = (500,300)
        
        self.planets = []
        self.currentPlanet = None
        self.updateArea = []
        self.mode = 'draw'
        
        self.legend = [ 'H: hide/show the legend',
                        'D: draw planets',
                        'E: erase planets',
                        'R: resize planets',
                        'M: move planets',
                        'T: set start point',
                        'O: set rotation: ',
                        'P: draw meteor path: ',
                        'G: set the goal',
                        'L: remove the last path',
                        '0-9: set rotation/meteor speed',
                        '-: set rotation direction',
                        'S: save',
                        'A: load',
                        'N: set file name: ']
        self.showLegend = 1
        self.rotationSpeed = 0
        self.paths = []
        self.currentPath = []
        self.goalPlanet = None
        self.legendIndex = 1
        
        self.legendSelectIndex = 0
        
        self.ll = levelLoader()
        
        
            
    def load(self):
        if self.file:
            level = None
            
            try:
                level = self.ll.loadLevel(os.path.join('custom',self.file + '.frog'),1)
            except:
                pass
            
            if level:
                self.planets = level.p
                self.paths = level.m
                self.startPoint = level.s
    
    def run(self):
        go = 1
        while go:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(1)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                            sys.exit(1)
                    elif self.mode == 'naming':
                        if event.key == K_RETURN:
                            self.mode = 'draw'
                            self.legendIndex = 1
                        elif event.key == K_BACKSPACE:
                            if self.file:
                                self.file = self.file[:-1]
                        else:
                            self.file += event.unicode
                    else:
                        if event.key == K_m:
                            self.mode = 'move'
                            self.legendIndex = 4
                        elif event.key == K_d:
                            self.mode = 'draw'
                            self.legendIndex = 1
                        elif event.key == K_r:
                            self.mode = 'resize'
                            self.legendIndex = 3
                        elif event.key == K_e:
                            self.mode = 'erase'
                            self.legendIndex = 2
                        elif event.key == K_s:
                            self.save()
                        elif event.key == K_t:
                            self.legendIndex = 5
                            self.mode = 'start'
                        elif event.key == K_o:
                            self.legendIndex = 6
                            self.mode = 'rotate'
                        elif event.key == K_MINUS:
                            self.rotationSpeed *= -1
                        elif event.key == K_p:
                            self.mode = 'path'
                            self.legendIndex = 7
                        elif event.key == K_g:
                            self.mode = 'goal'
                            self.legendIndex = 8
                        elif event.key == K_l:
                            if self.paths:
                                self.paths.remove(self.paths[-1])
                        elif event.key == K_h:
                            self.showLegend = not self.showLegend
                        elif event.key == K_a:
                            self.load()
                        elif event.key == K_n:
                            self.mode = 'naming'
                            self.legendIndex = 14
                        elif event.key == K_DOWN:
                            self.legendSelectIndex = (self.legendSelectIndex + 1) % len(self.legend)
                        elif event.key == K_UP:
                            self.legendSelectIndex = (self.legendSelectIndex - 1) % len(self.legend)
                        elif event.key == K_RETURN:
                            if self.showLegend:
                                if self.legendSelectIndex == 4:
                                    self.mode = 'move'
                                    self.legendIndex = 4
                                elif self.legendSelectIndex == 1:
                                    self.mode = 'draw'
                                    self.legendIndex = 1
                                elif self.legendSelectIndex == 3:
                                    self.mode = 'resize'
                                    self.legendIndex = 3
                                elif self.legendSelectIndex == 2:
                                    self.mode = 'erase'
                                    self.legendIndex = 2
                                elif self.legendSelectIndex == 12:
                                    self.save()
                                elif self.legendSelectIndex == 5:
                                    self.legendIndex = 5
                                    self.mode = 'start'
                                elif self.legendSelectIndex == 6:
                                    self.legendIndex = 6
                                    self.mode = 'rotate'
                                elif self.legendSelectIndex == 11:
                                    self.rotationSpeed *= -1
                                elif self.legendSelectIndex == 7:
                                    self.mode = 'path'
                                    self.legendIndex = 7
                                elif self.legendSelectIndex == 8:
                                    self.mode = 'goal'
                                    self.legendIndex = 8
                                elif self.legendSelectIndex == 9:
                                    if self.paths:
                                        self.paths.remove(self.paths[-1])
                                elif self.legendSelectIndex == 0:
                                    self.showLegend = not self.showLegend
                                elif self.legendSelectIndex == 13:
                                    self.load()
                                elif self.legendSelectIndex == 14:
                                    self.mode = 'naming'
                                    self.legendIndex = 14
                        try:
                            i = int(event.unicode)
                            if self.rotationSpeed:
                                self.rotationSpeed = self.rotationSpeed / abs(self.rotationSpeed) * i
                            else:
                                self.rotationSpeed = i
                        except:
                            pass
                elif event.type == MOUSEBUTTONUP:
                    if self.mode == 'drawing':
                        rad = (self.finalPoint - self.initialPoint).get_length()
                        self.planets.append(self.currentPlanet)
                        self.currentPlanet = None
                        self.currentImage = (self.currentImage + 1) % len(self.images)
                        self.mode = 'draw'
                    elif self.mode == 'moving':
                        self.mode = 'move'
                    elif self.mode == 'resizing':
                        self.mode = 'resize'
                    elif self.mode == 'pathing':
                        self.mode = 'path'
                        self.paths.append(self.currentPath)
                        self.currentPath = []
                    elif self.mode == 'goaling':
                        for p in self.planets:
                            p.goal = -1
                            p.ang = 0
                        self.mode = 'goal'
                        p = vec2d(event.pos[0],event.pos[1])
                        goalang = (p - self.goalPlanet.pos).get_angle()
                        self.goalPlanet.goal = goalang
                elif event.type == MOUSEBUTTONDOWN:
                    if self.mode == 'draw':
                        self.initialPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.finalPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.currentPlanet = planet(self.initialPoint,0,self.rotationSpeed)
                        self.currentPlanet.imageIndex = self.currentImage
                        self.mode = 'drawing'
                    elif self.mode == 'move':
                        self.movep = self.getPlanet(vec2d(\
                                event.pos[0],event.pos[1]))
                        self.finalPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.movep.pos = self.finalPoint
                        self.mode = 'moving'
                    elif self.mode == 'resize':
                        self.resizep = self.getPlanet(vec2d(\
                                event.pos[0],event.pos[1]))
                        self.finalPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.resizep.rad = (self.resizep.pos - self.finalPoint).get_length()
                        self.mode = 'resizing'
                    elif self.mode == 'erase':
                        if self.planets:
                            self.planets.remove(self.getPlanet(vec2d(\
                                event.pos[0],event.pos[1])))
                    elif self.mode == 'start':
                        self.startPoint = event.pos
                    elif self.mode == 'rotate':
                        self.getPlanet(vec2d(event.pos[0],event.pos[1])).rot = self.rotationSpeed
                    elif self.mode == 'path':
                        self.currentPath = [event.pos]
                        if not self.rotationSpeed:
                            self.rotationSpeed = 5
                        self.mode = 'pathing'
                    elif self.mode == 'goal':
                        self.goalPlanet = self.getPlanet(vec2d(event.pos[0],event.pos[1]))
                        self.mode = 'goaling'
                elif event.type == MOUSEMOTION:
                    if self.mode == 'drawing':
                        self.finalPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.currentPlanet.rad = (self.initialPoint - self.finalPoint).get_length()
                    elif self.mode == 'moving':
                        self.finalPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.movep.pos = self.finalPoint
                    elif self.mode == 'resizing':
                        self.finalPoint = vec2d(\
                                event.pos[0],event.pos[1])
                        self.resizep.rad = (self.resizep.pos - self.finalPoint).get_length()
                    elif self.mode == 'pathing':
                        self.updatePath(event.pos)
            for p in self.planets:
                p.ang = (p.ang + p.rot) % 360
                self.drawPlanet(p)
            if self.currentPlanet:
                self.drawPlanet(self.currentPlanet)
            for p in self.paths:
                self.drawPath(p)
            if self.currentPath:
                self.drawPath(self.currentPath)
            self.updateArea.append(pygame.draw.circle(self.screen,(255,0,0),self.startPoint,10))
            self.drawLegend()
            pygame.display.update(self.updateArea)
            self.updateArea = []
            self.eraseLegend()
            for p in self.paths:
                self.erasePath(p)
            if self.currentPath:
                self.erasePath(self.currentPath)
            for p in self.planets:
                self.erasePlanet(p)
            if self.currentPlanet:
                self.erasePlanet(self.currentPlanet)
            self.updateArea.append(pygame.draw.circle(self.screen,(0,0,0),self.startPoint,10))
            
		        
    def updatePath(self,point):
        if self.currentPath:
            l = vec2d(self.currentPath[-1])
            p = vec2d(point)
            d = p - l
            if d.get_length() > abs(self.rotationSpeed):
                d.length = abs(self.rotationSpeed)
                n = l + d
                self.currentPath.append(n.tup())
                self.updatePath(point)
        else:
            self.currentPath.append(point)
    
    def drawPlanet(self,p):
        c,r,i = p.pos.tup(),p.rad,p.imageIndex
        s = round(2 * r / 0.96) #magic
        tempi = pygame.transform.rotate(pygame.transform.scale(self.images[i],(s,s)),p.ang)
        rect = tempi.get_rect()
        rect.center = c
        self.updateArea.append(self.screen.blit(tempi,rect))
        if p.goal != -1:
            v = vec2d(p.rad, 0)
            v.rotate(-p.ang + p.goal)
            x = p.pos + v
            self.updateArea.append(pygame.draw.circle(self.screen, (0,255,0), x.inttup(), 40, 1))

    def erasePlanet(self,p):
        c,r,i = p.pos.tup(),p.rad,p.imageIndex
        s = round(2 * r / 0.96) #magic
        rect = pygame.Rect(0,0,s,s)
        rect.center = c
        self.updateArea.append(pygame.draw.rect(self.screen,(0,0,0),rect))
        if p.goal != -1:
            v = vec2d(p.rad, 0)
            v.rotate(-p.ang + p.goal)
            x = p.pos + v
            self.updateArea.append(pygame.draw.circle(self.screen, (0,0,0), x.inttup(), 40, 1))
        
        
    def drawPath(self,p):
        if len(p) > 1:
            self.updateArea.append(pygame.draw.lines(self.screen,(0,255,255),1,p))
        for point in p:
            self.updateArea.append(pygame.draw.circle(self.screen,(0,255,255),point,2))
    
    def erasePath(self,p):
        if len(p) > 1:
            self.updateArea.append(pygame.draw.lines(self.screen,(0,0,0),1,p))
        for point in p:
            self.updateArea.append(pygame.draw.circle(self.screen,(0,0,0),point,2))
    
    
    def drawLegend(self):
        if self.showLegend:
            for i in range(len(self.legend)):
                s = self.legend[i]
                if i == 6:
                    s = s + `self.rotationSpeed`
                if i == 7:
                    s = s + `abs(self.rotationSpeed)`
                if i == 14:
                    s = s + self.file
                c = (255,255,255)
                if i == self.legendIndex:
                    c = (0,255,255)
                f = drawFont(s, c)
                r = f.get_rect()
                r.left = 50
                r.top = 50+i*r.height
                self.updateArea.append(self.screen.blit(f,r))
                if self.legendSelectIndex == i:
                    p = (45,50 + (i+0.5) * r.height)
                    self.updateArea.append(pygame.draw.circle(self.screen,(255,0,0),p,4))
        else:
            s = self.legend[0]
            c = (255,255,255)
            f = drawFont(s, c)
            r = f.get_rect()
            r.left = 50
            r.top = 50
            self.updateArea.append(self.screen.blit(f,r))
            
    def eraseLegend(self):
        m = 0
        h = 0
        for i in range(len(self.legend)):
            s = self.legend[i]
            if i == 14:
                s = s + self.file
            f = drawFont(s)
            r = f.get_rect()
            h = r.height
            m = max(m,r.width)
            if self.legendSelectIndex == i:
                    p = (45,50 + (i+0.5) * r.height)
                    self.updateArea.append(pygame.draw.circle(self.screen,(0,0,0),p,4))
        rect = pygame.Rect(50,50,m,h*len(self.legend))
        self.updateArea.append(pygame.draw.rect(self.screen,(0,0,0),rect))
        
        
    def getPlanet(self,point):
        min = 0
        minp = None
        for p in self.planets:
            if minp:
                d = (point - p.pos).get_length()
                if d < min:
                    minp = p
                    min = d
            else:
                minp = p
                min = (point - p.pos).get_length()
        return minp
    
    def save(self):
        if self.file:
            planets = []
            goali = 0
            goal = 0
            for i in range(len(self.planets)):
                p = self.planets[i]
                a = (p.pos.tup(),p.rad,p.imageIndex,p.rot)
                planets.append(a)
                if p.goal != -1:
                    goali = i
                    goal = p.goal
            s = `planets`
            file = open(os.path.join('custom',self.file + '.frog'),'w')
            file.write(s)
            file.write('\n')
            file.write(`(goali,goal)`)
            file.write('\n')
            file.write(`self.startPoint`)
            file.write('\n')
            file.write(`self.paths`)
            file.write('\n')

        
if __name__ == '__main__':

    if len(sys.argv) == 2:
        file = sys.argv[1]
    else:
        file = 'save'
        
    le = levelEditor(file)
    le.run()
