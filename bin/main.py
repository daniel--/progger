import pygame, sys
from os import listdir
from os.path import join
from pygame.locals import *
from math import sqrt, e, log, atan2
from random import uniform, normalvariate
from level import *
from frog import *
from vec2d import *
from levelloader import *
from leveleditor import drawFont

class progger:
    def __init__(self):

        self.w = 1024
        self.h = 768
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill((0,0,0))
        self.dt = 1
        self.ll = levelLoader()
        
        self.levelList = []
        self.c = 0
        
        self.selected = 0 #the thing selected in levelList
        self.inMainMenu = True
        
        self.zingSound = pygame.mixer.Sound('ZING.WAV')
        self.enterSound = pygame.mixer.Sound('SPACCODE.WAV') 
        self.jumpSound = pygame.mixer.Sound('SPACEBO.WAV')
        self.jumpSound.set_volume(0.5)
        
        self.lookPath = join(sys.path[0], 'campaign') #where i list .frog files from in main menu
        
        self.message= ""
        self.startMessage = 0
        self.messageDuration = 0
        self.drawMessage = False
        
        self.clockObj = pygame.time.Clock()
        self.levels = 22 #number of levels in the whole game
        self.jumps= []
        self.numJumps = 0
        self.currentLevel = 0
        self.loadInfo()
        
    def loadInfo(self):
        z = open("status", 'r')
        self.jumps = []
        k = z.readlines()
        for j in k:
            self.jumps.append(int(j))
        z.close()
        
    def saveInfo(self):
        z = open("status", 'w')
        for k in self.jumps:
            z.write(`k` + '\n')
            
    def quitGame(self):
        self.saveInfo()
        sys.exit(1)
        
    def makeMessage(self, msg, duration=100):
        self.message = msg
        self.startMessage = self.c
        self.messageDuration = duration
        self.drawMessage = True
        
    def reloadLevel(self, name):
        
        self.level = self.ll.loadLevel(join(self.lookPath,name) + '.frog')
        self.frog = frog(self.level.s, pygame.image.load('frog.png'))
        self.tongue = tongue()
        self.c = 0 #COUNTER
        self.goalPlanet = self.level.goalPlanet
        self.goalAngle = self.level.goalAngle
    
    def handle_input_menu(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quitGame()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quitGame()
                elif event.key == K_DOWN:
                    if self.selected < len(self.levelList) -1:
                        self.selected +=1
                    else:
                        self.selected = 0
                    self.zingSound.play()
                elif event.key == K_UP:
                    if self.selected > 0:
                        self.selected -=1
                    else:
                        self.selected = len(self.levelList) - 1
                    self.zingSound.play()
                elif event.key == K_SPACE:
                    if self.lookPath == join(sys.path[0], 'campaign'):
                        self.lookPath = join(sys.path[0], 'custom')
                    else:
                        self.lookPath = join(sys.path[0], 'campaign')
                    
                    self.loadLevelList()
                elif event.key == K_RETURN:
                    self.drawMessage = False
                    #check if its unlocked first
                    if (self.lookPath == join(sys.path[0], 'custom')
                        or (self.selected ==0 or self.jumps[self.selected -1] >0)):
                        
                        #run the selected level
                        self.reloadLevel(self.levelList[self.selected])
                        self.inMainMenu = False
                        self.enterSound.play()
                        if self.lookPath == join(sys.path[0], 'campaign'):
                            self.currentLevel = self.selected
                            self.numJumps = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quitGame()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.inMainMenu = True
                    self.drawMessage = False
                    
                elif event.key == K_SPACE:
                    if self.frog.planet:
                        self.frog.jumpStrength = 0
                        self.frog.jumpStart = self.c - 2
                        self.frog.jumping = True
                        self.numJumps += 1
                    
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    if self.frog.planet:
                        self.frog.jumping = False
                        self.frog.jumpThisFrame = True
                        self.jumpSound.play()
                        
                elif event.key == K_r:
                    #rest frog position
                    self.reloadLevel(self.levelList[self.selected])
                    self.numJumps = 0
                
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    #FIRE THE TONGUE!!!
                    if self.tongue.vel == None:
                        v = vec2d(event.pos) - self.frog.pos
                        v.length = 25
                        self.tongue.vel = v
                        self.tongue.pos = vec2d(self.frog.pos.tup())
                else:
                    #LET GO OF THE TONGUE
                    if self.tongue.vel != None:
                        #tongue is fired, retract it
                        self.tongue.vel = None
                        self.tongue.latched = None
                        
    def draw_menu(self):
        i = 20
        
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0,0,300, 768))
        t = drawFont("Choose Level:", (0,255,255))
        self.screen.blit(t, (50, 0))
        OMG=0
        for f in self.levelList:
            x=""
            c=(255,0,0)
            if self.lookPath == join(sys.path[0], 'campaign'):
                if self.jumps[OMG] > 0 or OMG == 0 or self.jumps[OMG-1] >0:
                    if self.jumps[OMG] > 0:
                        x= " [min jumps: " + `self.jumps[OMG]` + "]"
                    c=(0,255,100)
                OMG+=1
                
            if self.lookPath == join(sys.path[0], 'campaign'):
                z = drawFont(f + x, color =c)
            else:
                z = drawFont(f + x)
                
            if self.selected == (i-1)/20:
                r = z.get_rect()
                r= r.move(50, i)
                r=r.inflate(15, -10)
                pygame.draw.rect(self.screen, (150,0,0), r)
                
            self.screen.blit(z, (50, i))
            i+= 20
            
        pygame.display.flip()
        
    def draw(self):
    
        #draw the background
        self.screen.fill((0,0,0))
    
        #draw meteor path
        for m in self.level.m:
            i=0
            for i in range(len(m.moveList)-1):
                pygame.draw.line(self.screen, (0,100,100), m.moveList[i], m.moveList[i+1], 1)
            pygame.draw.line(self.screen, (0,100,100), m.moveList[0], m.moveList[len(m.moveList)-1], 1)
            
        #draw planets and meteors
        for p in self.level.pm:
            c = p.rect.center
            surf = pygame.transform.rotate(p.image, p.ang)
            newrect = surf.get_rect()
            newrect.center = c
            self.screen.blit(surf, newrect)
            #pygame.draw.circle(self.screen, (255,0,0), p.pos, p.rad, 1)
            
        #draw frog
        c = self.frog.rect.center
        s = pygame.transform.rotate(self.frog.image, self.frog.ang)
        newrect = s.get_rect()
        newrect.center = c
        self.screen.blit(s, newrect)
        p = (int(self.frog.pos[0]), int(self.frog.pos[1]))
        pygame.draw.circle(self.screen, (255,0,0), p, 0)
        
        #if the frog is outside of the screen draw a small indicator
        if not pygame.Rect(0,0,1024,768).collidepoint(self.frog.pos.inttup()):
            x = self.frog.pos.x
            y = self.frog.pos.y
            cx = min(max(x, 10), 1014)
            cy = min(max(y, 10), 738)
            pygame.draw.circle(self.screen, (0, 255, 0), (int(cx), int(cy)), 5)
                               
        #draw tongue
        v=vec2d(10,0)
        v.rotate(-self.frog.ang-90)
        p = (self.frog.pos + v).inttup()
        if self.tongue.latched != None:
            pygame.draw.line(self.screen, (255,0,0), p, self.tongue.latched.pos.inttup(), 3)
        else:
            if self.tongue.vel != None:
                pygame.draw.line(self.screen, (255,0,0), p, self.tongue.pos.inttup(), 3)
        
        #draw Goal
        v = vec2d(self.goalPlanet.rad, 0)
        v.rotate(-self.goalPlanet.ang + self.goalAngle)
        x = self.goalPlanet.pos + v
        pygame.draw.circle(self.screen, (0,255,0), x.inttup(), 40, 1)
        
        a = self.w - 50
        b = self.h - 40
        pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(a, b, 30, -self.frog.jumpStrength*10))
        
        #draw message
        if self.drawMessage:
            m = drawFont(self.message)
            self.screen.blit(m, (300,100))
            
        pygame.display.flip()

    def accumAcc(self):
        acc = vec2d(0,0)
        
        if self.tongue.latched:
            d = self.tongue.latched.pos.get_distance(self.frog.pos)
            dx = self.tongue.dist - d
            v = self.tongue.latched.pos - self.frog.pos
            v.length = self.tongue.k*dx
            acc += -v
            
        if self.frog.jumpThisFrame:
            if self.frog.planet:
                v = self.frog.pos - self.frog.planet.pos
                v.length = self.frog.jumpStrength
                acc += v        
                self.frog.planet = None
                self.frog.jumping = False
                self.frog.jumpThisFrame = False
                
        for p in self.level.p:
            #F = GM/r^2
            d = self.frog.pos.get_dist_sqrd(p.pos)
            m = p.rad*p.rad
            a = 1.5*m/d #scaling factor lol
            v = p.pos - self.frog.pos
            v.length = a
            acc += v
        
        if self.frog.planet == None:    
            self.frog.acc = acc
        
    def verlet(self):
        temp = vec2d(self.frog.pos.tup())
        self.frog.pos += self.frog.pos - self.frog.oldpos + self.frog.acc*self.dt*self.dt
        self.frog.oldpos = temp
        self.frog.rect.center = self.frog.pos
        
    def frogTick(self):
        
        if self.tongue.latched != None:
            if self.tongue.latched.pos.get_distance(self.frog.pos) > 300:
                self.tongue.vel = None
                self.tongue.latched = None
            
        #take care of tongue
        if self.tongue.vel != None:
            if self.tongue.latched == None:
                self.tongue.pos += self.tongue.vel
                if self.tongue.pos.get_distance(self.frog.pos) < 300:
                    
                    for m in self.level.m:
                        if m.pos.get_distance(self.tongue.pos) < 50:
                            self.tongue.latched = m
                            self.tongue.dist = 0 #self.tongue.pos.get_distance(self.frog.pos)
                            break
                else:
                    self.tongue.vel = None #retract it
                
        #take care of jumping
        if self.frog.jumping:
            self.frog.jumpStrength = self.c - self.frog.jumpStart
            if self.frog.jumpStrength > 15:
                self.frog.jumpStrength = 15
            
        #now set the frogs target angle
        if self.frog.planet:
            v = self.frog.pos - self.frog.planet.pos
            self.frog.tang = 270 - v.get_angle()
        else:
            v = self.frog.pos - self.frog.oldpos
            self.frog.tang = 90 - v.get_angle()
        
        f = self.frog
        while abs(f.tang - f.ang) > 180:
            if f.ang > f.tang:
                f.tang += 360
            else:
                f.tang -= 360
        
        if abs(f.tang - f.ang) > f.angIncr:
            if f.tang > f.ang:
                f.ang += f.angIncr
            else:
                f.ang -= f.angIncr
        else:
            f.ang = f.tang
            
        #check for goal condition
        if self.frog.planet == self.level.goalPlanet:
            v = vec2d(self.goalPlanet.rad, 0)
            v.rotate(-self.goalPlanet.ang + self.goalAngle)
            x = self.goalPlanet.pos + v
            if self.frog.pos.get_distance(x) < 40:
                if self.selected == 22:
                    self.makeMessage("YOU WIN! The ProgFrog has reached Earth and freed it's brethren. Congratulations.")
                else:
                    self.makeMessage("You beat the level in " + `self.numJumps` + " jumps! Next level was unlocked." )
                if self.jumps[self.selected] == 0:
                    self.jumps[self.selected] = self.numJumps
                else:
                    self.jumps[self.selected] = min(self.numJumps, self.jumps[self.selected])
                
    def planetTick(self):
        for p in self.level.pm:
            p.ang += p.angIncr
            if p == self.frog.planet:
                v = self.frog.pos - p.pos
                v.rotate(-p.angIncr)
                self.frog.pos = p.pos + v
                self.frog.oldpos = p.pos + v
        
        for m in self.level.m:
            #move meteors
            m.pos = vec2d(m.moveList[m.moveIndex])
            m.rect.center = m.pos
            m.moveIndex += 1
            if m.moveIndex >= len(m.moveList):
                m.moveIndex = 0
            
    def collide(self):
        for p in self.level.p:
            if self.frog.pos.get_distance(p.pos) < p.rad + 20:
                #collision!
                v = self.frog.pos - p.pos
                v.length = p.rad + 20
                self.frog.pos = p.pos + v
                self.frog.oldpos = p.pos + v
                self.frog.acc = 0
                self.frog.planet = p
                break
        
    def gameLoop(self):
        
        while 1:
            self.clockObj.tick(25)
            
            self.c += 1
            self.handle_input()
            
            #update all planets by rotating them
            self.planetTick()
            
            #rotate the frog
            self.frogTick()
            
            self.accumAcc()
            self.verlet()
            self.collide()
            
            self.draw()
            
            if self.c - self.startMessage  > self.messageDuration:
                self.drawMessage = False
                
            if self.inMainMenu == True:
                break
    
    def loadLevelList(self):
        self.levelList = []
        files = listdir(self.lookPath)
        for f in files:
            if f[-5:] == ".frog":
                self.levelList.append(f[:-5])
        
        self.levelList.sort()
    def menuLoop(self):
        #load the files that end with .frog
        
        self.loadLevelList()
        b = pygame.image.load("bck.bmp")
        self.screen.blit(b, (0,0))
        
        while self.inMainMenu:
            pygame.time.wait(30)
            self.handle_input_menu()
            self.draw_menu()
            self.c += 1
            
    def run(self):
        while 1:
            self.menuLoop()
            self.gameLoop()
            
        
p = progger()
p.run()
