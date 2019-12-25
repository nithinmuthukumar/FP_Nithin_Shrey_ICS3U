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
        self.dx,self.dy,self.dist,self.timer,self.fuse,self.speed = dx,dy,dist,0,fuse,speed
        self.deploy,self.explode,self.timer,self.bombmove = False,True,0,True
        self.vx,self.vy = 3.5,-1.5
        self.getdir = "None"
    def explodetimer(self,timer,fuse=3000):
        self.timer+=timer
        if self.timer > self.fuse:
            self.explode,self.bombmove = True,True
            self.deploy,self.vy = False,-1.5
            self.timer = 0
            self.rect.x,self.rect.y = player.rect.x,player.rect.y
    def update(self):
        if e.type==KEYUP and e.key==K_b:#self.shoot:
            if not self.deploy and self.explode:
                self.rect.x,self.rect.y = player.rect.x,player.rect.y
                self.deploy,self.explode = True,False
                if player.playermovement!=None:
                    self.totalpos,self.getdir = (player.rect.x,player.rect.y),player.playermovement
        if self.deploy:
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
                self.explode = False
            if self.getdir=="Right"  and self.rect.y<=self.totalpos[1] and self.rect.x+self.speed<800 and self.bombmove:#and self.rect.x+self.speed<self.totalpos[0]+self.dist and self.rect.x+self.speed<800 and self.bombmove:
                self.vy+=0.05
                self.rect.x+=self.vx
                self.rect.y+=self.vy
                if self.rect.y>self.totalpos[1]:
                    self.bombmove,self.explode = False,False
player = player()
player.rect.x,player.rect.y = 20,20
bomb = bomb(40,200,50)
clock = time.Clock()
while not done:
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    deltatime = clock.tick(60)/1000.0
    for e in event.get():
        if e.type==QUIT:
            done = True
    if bomb.deploy:
        bomb.explodetimer(clock.get_time())
    keys = key.get_pressed()
    player.keys()
    screen.fill((255,255,255))
    screen.blit(player.playersprite,(player.rect.x,player.rect.y))
    bomb.update()
    if bomb.deploy and not bomb.explode:
        screen.blit(bomb.image,(bomb.rect.x,bomb.rect.y))
    display.flip()
quit()
