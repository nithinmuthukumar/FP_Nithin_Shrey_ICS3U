from pygame import *
import math
import os 
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
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
coords = 400, 200
angle = 0
speed = 1
next_tick = 500
increment = 2

def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)

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
        if e.type==KEYUP:
            if e.key==K_UP:
                increment+=1
            if e.key==K_DOWN and increment-1!=0:
                increment-=1
    keys = key.get_pressed()
    ticks = time.get_ticks() 
    if ticks > next_tick:
        next_tick += speed
        angle += 1
        coords = move_coords(angle, increment, coords)
    if not keys[K_SPACE]:
        screen.fill(0)#(255,255,255))
    screen.blit(image,(coords[0],coords[1]))
    #draw.circle(screen,(0,255,0),(int(ballX),int(ballY)),20)
    display.flip()
    image = strips[n].next()
    clock.tick(FPS)
quit()
