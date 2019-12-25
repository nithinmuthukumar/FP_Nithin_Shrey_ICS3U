from pygame import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
screen = display.set_mode((800,740))
display.set_caption("Bomb Test")
done = False
class player(object):
    def __init__(self,speed=3):
        self.speed = speed
        self.playermovement = "None"
        self.movex = 0
        self.movey = 0
        self.playersprite = image.load("player.png").convert()
        self.playersprite.set_colorkey((255,255,255))
        self.playersprite = transform.scale(self.playersprite,(20,20))
        self.rect = self.playersprite.get_rect()
    def keys(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y-=self.speed
            self.playermovement = "Up"
        if keys[K_a]:
            self.rect.x-=self.speed
            self.playermovement = "Left"
        if keys[K_s]:
            self.rect.y+=self.speed
            self.playermovement = "Down"
        if keys[K_d]:
            self.rect.x+=self.speed
            self.playermovement = "Right"
        if not keys[K_w] and not keys[K_a] and not keys[K_s] and not keys[K_d]:
            self.playermovement = None

class bomb():
    def __init__(self,dx=5,dy=3,dist=200,fuse=3000,speed=5):
        self.image = image.load("bomb.png").convert()
        self.image.set_colorkey((255,255,255))
        self.image = transform.scale(self.image,(20,20))
        self.bombsurf = screen.subsurface(screen.get_rect())
        self.rect = self.image.get_rect()
        #self.rect.x,self.rect.y = player.rect.x,player.rect.y
        self.dx,self.dy,self.dist,self.timer,self.fuse,self.speed = dx,dy,dist,0,fuse,speed
##        self.shoot,self.deploy,self.explode,self.timer = False,False,False,0
        self.deploy,self.explode,self.timer,self.bombmove = False,True,0,True
        self.vx,self.vy = 5,-0.5
        self.getdir = "None"
##    def deployed(self):
##        if e.type==KEYUP and e.key==K_b:
##            self.shoot = True
##            print(True)
    def explodetimer(self,timer,fuse=3000):
        self.timer+=timer
        if self.timer > self.fuse:
            self.explode,self.bombmove = True,True
            self.deploy,self.vy = False,-0.5
            self.timer = 0
            self.rect.x,self.rect.y = player.rect.x,player.rect.y
            print(True)
##    def killrange(self):
##        "sprite kill code goes here"
##        self.bombsurf.update((self.rect.x-25,self.rect.y-25,50,50))

##    def rightparabola(x,y,stretch,vertexy):
##        self.returny = strech*x-vertexy
##        x = range(-10,10)
##        y = []
##        a = 2 # this is the positive or negative curvature
##        h = player.rect.x+50 # horizontal offset: make this term +/- to shift the curve "side to side"
##        k = player.rect.y+20 # vertical offset: make this term +/- to shift the curve "up to down"
##        for xi in x:
##            y.append(a * (xi - h)** 2 + k)
##        return list([(x,i) for x in range(-10,10) for i in y])
##    def leftparabola(self,x1,y=0,stretch=0,vertexy=0):
##        #self.returny = stretch*x-vertexy
##        #x = range(-x1,x1)
##        self.y = []
##        self.a = 0.0000000000000005 # this is the positive or negative curvature
##        self.h = player.rect.x-20 # horizontal offset: make this term +/- to shift the curve "side to side"
##        self.k = player.rect.y+20 # vertical offset: make this term +/- to shift the curve "up to down"
##        self.x1 = x1
##        for xi in range(-20,20):#(-self.x1,self.x1):
##            self.y.append(self.a * (xi + self.h)** 2 + self.k)
##        return [(x,i) for x in range(-20,20) for i in self.y]#(-x1,x1) for i in self.y])
        """
        Define what set of points will be chosen -- return a list that the update function runs through?
        make sure it returns path for going both left and right
        Why should I use y?
        How to use x+verterx y? playerx/playery + selfx,selfy?
        """
#        self.returnx = 
    def update(self):
##        print(self.bombmove)
        if e.type==KEYUP and e.key==K_b:#self.shoot:
##            print(True)
            if not self.deploy and self.explode:
                self.rect.x,self.rect.y = player.rect.x,player.rect.y
                self.deploy,self.explode = True,False
                if player.playermovement!=None:
                    self.totalpos,self.getdir = (player.rect.x,player.rect.y),player.playermovement
                    print(self.rect.y,self.totalpos[1])
                """ 
                Replace with bound function
                """
##                if player.playermovement=="Up":
##                    self.rect.x = player.rect.x
##                    if self.rect.y<player.rect.y-20:
##                        print(self.rect.y-3,player.rect.y-20)
##                        self.rect.y-=3
##                    self.deploy,self.explode = True,False
        if self.deploy:
            #print(self.rect.y,self.totalpos)
            if self.getdir=="Up" and self.rect.y-self.speed>self.totalpos[1]-self.dist and self.rect.y-self.speed>0:
                self.rect.y-=self.speed
                self.explode = False
            if self.getdir=="Down" and self.rect.y+self.speed<self.totalpos[1]+self.dist and self.rect.y+self.speed<725:
                self.rect.y+=self.speed
                self.explode = False
            if self.getdir=="Left" and self.rect.y<=self.totalpos[1] and self.rect.x-self.speed>0 and self.bombmove:#and self.rect.x-self.speed>self.totalpos[0]-self.dist and self.rect.x-self.speed>0 and self.bombmove:
                self.vy+=0.05
                self.rect.x-=self.vx
                self.rect.y+=self.vy
                if self.rect.y>self.totalpos[1]:
                    self.bombmove,self.explode = False,False
##                print(player.rect.x)
##                self.pos = self.leftparabola(player.rect.x)
##                print(self.pos)

                #self.rect.x,self.rect.y = (pos)
#                self.rect.x-=5
                self.explode = False
            if self.getdir=="Right"  and self.rect.y<=self.totalpos[1] and self.rect.x+self.speed<800 and self.bombmove:#and self.rect.x+self.speed<self.totalpos[0]+self.dist and self.rect.x+self.speed<800 and self.bombmove:
                self.vy+=0.05
                self.rect.x+=self.vx
                self.rect.y+=self.vy
                if self.rect.y>self.totalpos[1]:
                    self.bombmove,self.explode = False,False
##            if self.deploy and not self.explode:
##                screen.blit(self.image,(self.rect.x,self.rect.y))
##                self.explode = False
player = player()
player.rect.x,player.rect.y = 20,20
bomb = bomb(40,200)
clock = time.Clock()
while not done:
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    deltatime = clock.tick(60)/1000.0
    for e in event.get():
        if e.type==QUIT:
            done = True
##        if e.type==KEYUP and e.key==K_b:
##            bomb.shoot = True
    if bomb.deploy:
        bomb.explodetimer(clock.get_time())
    keys = key.get_pressed()
    player.keys()
#    if keys[K_f]:
    screen.fill((255,255,255))
    screen.blit(player.playersprite,(player.rect.x,player.rect.y))
    bomb.update()
    if bomb.deploy and not bomb.explode:
        screen.blit(bomb.image,(bomb.rect.x,bomb.rect.y))
    display.flip()
quit()
