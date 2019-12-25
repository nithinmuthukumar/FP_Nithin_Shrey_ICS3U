from pygame import *
import os 
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
from random import *
import spritesheet
from sprite_strip_anim import SpriteStripAnim

screen = display.set_mode((800,800))
FPS = 120
frames = FPS / 12
strips = [
    SpriteStripAnim('Explode1.bmp', (0,0,24,24), 8, (173,201,215), True, frames),
    SpriteStripAnim('Explode2.bmp', (0,0,24,24), 8, (0,0,0), True, frames)
]
horzmid,vertmid = screen.get_size()
horzmid = horzmid//2
vertmid = vertmid//2
ballX,ballY = horzmid,780
vx,vy = 5,-5
running = True
curve = False
clock = time.Clock()
n = 0
strips[n].iter()
image = strips[n].next()

class path():
    def __init__(self,sprite,startX,startY,vx,vy,xmax,xmin,ymax,ymin,curve=False):
        self.sprite, self.vx, self.vy, self.xmax, self.xmin, self.ymax, self.ymin, self.curve = sprite, vx, vy, xmax, xmin, ymax, ymin, curve
        self.rect = self.sprite.get_rect( center = (startX,startY))
    def move(self):
        self.rect.x+=vx
        if not self.curve:
            self.rect.y+=vy
        if self.curve:
            self.rect.y-=self.vy
        if self.rect.y>=self.ymax:
            self.curve = False
        if self.rect.y<=self.ymin and not self.curve:
            self.curve = True
        if self.rect.x>=self.xmax or self.rect.x<=self.xmin:
            self.vx*=-1

boomerang = path(image,horzmid,780,5,-5,780,20,780,20)


while running:
    #draw.circle(screen,(255,0,0),(int(ballX),int(ballY)),20)
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type==KEYUP and e.key==K_RETURN:
            n+=1
            if n>=len(strips):
                n = 0
            strips[n].iter()
    keys = key.get_pressed()
##    ballX+=vx
##    if not curve:
##        ballY+=vy
##    if curve:
##        ballY-=vy
##    if ballY>=780:
##        curve = False
##    if ballY<=20 and not curve:
##        curve = True
##    if ballX>=780 or ballX<=20:
##        vx*=-1
    screen.fill(0)#(255,255,255))
    boomerang.move()
    screen.blit(image,(boomerang.rect.x,boomerang.rect.y))##(int(ballX),int(ballY)))
    #draw.circle(screen,(0,255,0),(int(ballX),int(ballY)),20)
    display.flip()
    image = strips[n].next()
    clock.tick(FPS)
quit()
