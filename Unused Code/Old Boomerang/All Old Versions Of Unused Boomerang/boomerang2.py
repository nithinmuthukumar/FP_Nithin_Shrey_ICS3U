from pygame import *
from random import *

screen = display.set_mode((800,800))
horzmid,vertmid = screen.get_size()
horzmid = horzmid//2
vertmid = vertmid//2
ballX,ballY = horzmid,780
vx,vy = 5,-5#2,-2#10,-10#2,-5#20,-20,10,-1#2,-5#10,-2#10,-5#5,-2
#vx,vy = 20,-1 can be used to show enemy walk patterns
running=True
curve = False
while running:
    draw.circle(screen,(255,0,0),(int(ballX),int(ballY)),20)
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    keys = key.get_pressed()

    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    #vy += 0#.25
    ballX+=vx
    if not curve:
        ballY+=vy
    if curve:
        ballY-=vy
##    if ballY>10:
##        ballY-=vy
##        vy*=-0.9

##    if ballY>20 and curve:
##        #ballY-=vy
##        #vy*=1
##        if keys[K_SPACE]:
##            vy*=-1
##        if ballY==580:
##            curve = False
##            print(False)

    if ballY==780:
        curve = False
        print("Down; Going Up")


    if ballY==20 and not curve:
        #ballY+=vy
        curve = True
##        if keys[K_SPACE]:
##            vy*=-1
        print("Up; Going Down")
    if ballX==780 or ballX==20:#ballX>horzmid+100 or ballX<horzmid-100:
        #ballX-=vx
        vx*=-1#0.9
    #print(vx,vy)
    #screen.fill(0)
    draw.circle(screen,(0,255,0),(int(ballX),int(ballY)),20)
    display.flip()
    time.wait(10)
quit()
