from pygame import *
import math, os
from imageload import imageload
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"

class player(object):
    def __init__(self,speed=4):
        self.speed = speed
        self.playermovement = "None"
        self.movex = 0
        self.movey = 0
        self.playersprite = imageload("player.png",0.1,False,(255,255,255))
        self.rect = self.playersprite.get_rect()
    def keys(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>0:
            self.rect.y-=self.speed
            self.playermovement = "Up"
        if keys[K_a] and self.rect.x>0:
            self.rect.x-=self.speed
            self.playermovement = "Left"
        if keys[K_s] and self.rect.bottom<600:
            self.rect.y+=self.speed
            self.playermovement = "Down"
        if keys[K_d] and self.rect.right<800:
            self.rect.x+=self.speed
            self.playermovement = "Right"
        if not keys[K_w] and not keys[K_a] and not keys[K_s] and not keys[K_d]:
            self.playermovement = "None"

screen = display.set_mode((800,600))
display.set_caption("Minotaur")
done = False

class Minotaur():
    def __init__(self,pos,speed=2,stren=2):
        self.startx,self.starty,self.speed,self.stren,self.rushtime,self.tired,self.slowed = pos[0],pos[1],speed,stren,0,False,False
        self.phase = imageload("Phase1.png",1,False,(255,255,255))
        self.img = self.phase
        self.rect = self.img.get_rect()
        self.rect.x,self.rect.y = self.startx,self.starty
        self.hbar = imageload("HealthBar3.png",0.5,False,(255,255,255))
        self.hrect = self.hbar.get_rect()
        self.hrect.center = (screen.get_size()[0]//2,screen.get_size()[1]-35)
        self.hcounter = 47
##        self.hcounterrect = Rect(self.hrect.topleft[0]+40,self.hrect.topleft[1]+6,self.hrect.bottomright[0]-self.hrect.bottomleft[0]-self.hcounter,self.hrect.bottomright[1]-self.hrect.topright[1]-11)
##        print(self.rect.x)
    def phases(self,ap):
        """
        Use this in loop instead of directly putting Phase 1/2 in the loop
        """
        self.allphases = [i for i in range(ap)]
##        print(self.allphases,len(self.allphases))
    def rush(self,timer):
        #print(self.speed)
        self.rushtime+=timer
##        if self.tired:
##            self.speed = 0
##            if self.rushtime>2500:
##                self.tired,self.rushtime = False,0
##        if self.slowed:
##            self.speed = 2
##            print(True)
##            if self.rushtime>2500:
##                self.tired,self.slowed = True,False
##        if self.rushtime>2000 and not self.slowed and not self.tired:
##            self.speed = 5
##            if self.rushtime>4000:
##                self.speed,self.rushtime = 2,0
##                self.slowed = True
        if self.tired:
            self.speed = 0
            if self.rushtime>2500:
                self.tired,self.slowed,self.rushtime = False,True,0
        if self.slowed:
            self.speed = 2
##            print(True) 
            if self.rushtime>2500:
                self.tired,self.slowed = False,False
        if self.rushtime>2000 and not self.slowed and not self.tired:
            self.speed = 5
            if self.rushtime>4000:
                self.speed,self.rushtime = 2,0
                self.tired = True
    def patterns(self):
        pass
    def approach(self,player):
        x_dist = player.x - self.rect.x
        y_dist = player.y - self.rect.y
        return math.atan2(-y_dist, x_dist) % (2 * math.pi)
    def phase1(self):
        """
        [X] Chases you slowly, charges up and rushes you quickly, gets tired, then
        chases you slowly again.
        OR
        [ ] Chases you slowly for first cycle, chases you really fast, gets
        tired, slows down, then stops. Regains energy, chases you with burst of
        speed, gets tired, slows down, stops, etc.
        ^ This one is commented out ^
        """
        self.pos2 = self.approach(player.rect)
##        print(self.rect.x,self.rect.y)
        if not self.rect.collidepoint(player.rect.center):
            self.rect.x += (math.cos(self.pos2) * self.speed)
            self.rect.y -= (math.sin(self.pos2) * self.speed)
    def phase2(self):
        """
        Bull stays still, drops down projectiles on you, has a shield you must
        batter away and hit him once it drops, the shield regenerates as well.
        """
        pass
    def updatehealth(self):#,player):
        """
        Can't update in the class because will constantly happen in while loop
        --> KEYUP doesn't matter here
        """
##        try:
##            if self.rect.colliderect(player) and e.key==K_p and self.hcounter+1<=312:
##                self.hcounter+=1
##        except:
##            pass
        draw.rect(screen,(255,0,0),(self.hrect.topleft[0]+40,self.hrect.topleft[1]+6,self.hrect.bottomright[0]-self.hrect.bottomleft[0]-self.hcounter,self.hrect.bottomright[1]-self.hrect.topright[1]-11))#self.hcounterrect)
        screen.blit(self.hbar,self.hrect)
##def minoinit(pos):
##    MinoStartx,MinoStarty = pos
##    img = imageload("TestMinotaur.png",1,False,(255,255,255))
##    return img
##mino = minoinit((50,50))
##def timeupdate(timepass,time):
##    timepass+=time
##    if timepass > 1000:
##        timeinterval = True
##        timepass = 0
##    else:
##        timeinterval = False
##def mino(minohp):#(minohp=25):
##    if mino.colliderect(player.rect) and timeinterval:
####        minohp-=1
##        print(True)
##def phases(ap):
##    """
##    This is useless, no need to keep.
##    """
##    allphases = [i for i in range(ap)]
##    print(allphases,len(allphases))
##def patterns():
##    pass
####def phases():
####    if minohp>=totminohp//2:
####        phase1()
####    else:
####        phase2()
##def phase1():
##    pass
##def phase2():
##    pass

player = player()
player.rect.x = 20
player.rect.y = 20

mino = Minotaur((100,100))
phase2 = imageload("Phase2.png",1,False,(255,255,255))
mino.phases(2)
timepass = 0
clock = time.Clock()
while not done:
    for e in event.get():
        if e.type==QUIT:
            done = True
        if e.type==KEYUP:
            if e.key==K_j and mino.hcounter+5<=312:
                mino.hcounter+=5
            if e.key==K_k and mino.hcounter-5>=47:
                mino.hcounter-=5
            if mino.rect.colliderect(player.rect) and e.key==K_p and mino.hcounter+1<=312:
                mino.hcounter+=5
    changeintime = clock.tick(60)/1000.0
    player.keys()
    screen.fill((255,255,255))
    screen.blit(player.playersprite, (player.rect.x, player.rect.y))
##    timeupdate(timepass,clock.get_time())
##    phases()
##    screen.blit(mino,(50,50))
##    print(mino.hcounter)
    if mino.hcounter+5<=187:
        mino.rush(clock.get_time())
        mino.phase1()
        if mino.hcounter==182:
            mino.img = phase2
            mino.activatesecondphase = True
##    print(player.rect)
    mino.updatehealth()#player.rect)
    screen.blit(mino.img,(mino.rect.x,mino.rect.y))
    display.flip()
quit()
    
    
