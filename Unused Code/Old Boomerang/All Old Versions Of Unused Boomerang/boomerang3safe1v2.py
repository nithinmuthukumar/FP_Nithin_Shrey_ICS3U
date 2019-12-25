from pygame import *
from random import *
import spritesheet
from sprite_strip_anim import SpriteStripAnim

screen = display.set_mode((800,800))
FPS = 120
frames = FPS / 12
strips = [
    SpriteStripAnim('Explode7.bmp', (0,0,24,24), 8, (173,201,215), True, frames)
]
horzmid,vertmid = screen.get_size()
horzmid = horzmid//2
vertmid = vertmid//2
ballX,ballY = horzmid,780
vx,vy = 5,-5#2,-2#10,-10#2,-5#20,-20,10,-1#2,-5#10,-2#10,-5#5,-2
#vx,vy = 20,-1 can be used to show enemy walk patterns
running=True
curve = False
clock = time.Clock()
n = 0
strips[n].iter()
image = strips[n].next()
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
    if ballY==780:
        curve = False
    if ballY==20 and not curve:
        curve = True
##    if ballY<=400 and ballY>0 and ballX>=400 and ballX<=800 and not curve:
##        print("Quadrant 1")
##    if ballY<400 and ballY>0 and ballX>=200 and ballX<=400 and curve:
##        print("Quadrant 2")
##    if ballY>=400 and ballY<800 and ballX>0 and ballX<=400:
##        print("Quadrant 3")
##    if ballY>=400 and ballY<800 and ballX>=400 and ballX<800:
##        print("Quadrant 4")
    if ballX==780 or ballX==20:
        print("Sides")
        vx*=-1
    screen.fill(0)
    screen.blit(image,(int(ballX),int(ballY)))
    #draw.circle(screen,(0,255,0),(int(ballX),int(ballY)),20)
    display.flip()
    image = strips[n].next()
    clock.tick(FPS)
quit()
