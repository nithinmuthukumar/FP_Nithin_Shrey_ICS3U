from pygame import *
from random import *

screen = display.set_mode((800,600))
horzmid,vertmid = screen.get_size()
horzmid = horzmid//2
vertmid = vertmid//2
ballX,ballY = horzmid,550
vx,vy = 5,-5
running=True
curve = False
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    keys = key.get_pressed()

    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    vy += 0.25
    ballX+=vx
    if not curve:
        ballY-=vy
    if curve:
        ballY+=vy

    if ballY>10 and ballY<600 and curve:
        ballY+=vy
        vy*=0.9
        if ballY>580:
            curve = False
            print(False)
    if ballY<10 and not curve:
        ballY+=vy
        curve = True
        print(True)
    if ballX>horzmid+100 or ballX<horzmid-100:
        ballX-=vx
        vx*=-1

    screen.fill(0)
    draw.circle(screen,(255,0,0),(int(ballX),int(ballY)),20)
    display.flip()
    time.wait(10)
quit()
