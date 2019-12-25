from pygame import *
import math
screen = display.set_mode((400,400))
done = False
radius = 100
while not done:
    for e in event.get():
        if e.type==QUIT:
            done=True
    for angle in range(0,361):
            theta = math.radians(angle)
            x = radius*math.cos(theta)
            y = radius*math.sin(theta)
            x = int(x)
            y = int(y)

    draw.circle(screen,(0,255,0),(200+x,200+y),2)
            #print(x,y)

    display.flip()
quit()
