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
def hit(obj_rect,border):
    if border.contains(obj_rect):
        print("Collide")
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
    ballX+=vx
    if not curve:
        ballY+=vy
    if curve:
        ballY-=vy
    if ballY>=780:
        curve = False
    if ballY<=20 and not curve:
        curve = True
    if ballX>=780 or ballX<=20:
        vx*=-1
    screen.fill(0)#(255,255,255))
    screen.blit(image,(int(ballX),int(ballY)))
    hit(image.get_rect(),Rect(50,50,screen.get_size()[0]-50,screen.get_size()[1]-50))
    #draw.circle(screen,(0,255,0),(int(ballX),int(ballY)),20)
    display.flip()
    image = strips[n].next()
    clock.tick(FPS)
quit()
