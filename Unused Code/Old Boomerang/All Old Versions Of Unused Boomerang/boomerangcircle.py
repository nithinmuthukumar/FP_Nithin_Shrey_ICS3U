from pygame import *
import math
import os 
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
from random import *
import spritesheet
from sprite_strip_anim import SpriteStripAnim
FPS = 120
frames = FPS / 12
strips = [
    SpriteStripAnim('Explode1.bmp', (0,0,24,24), 8, (173,201,215), True, frames),
    SpriteStripAnim('Explode2.bmp', (0,0,24,24), 8, (0,0,0), True, frames)
]

screen = display.set_mode((800, 600))
display.set_caption("Boomerang")
coords = 400, 200
angle = 0
rect = Rect(*coords,20,20)
speed = 1
next_tick = 500

clock = time.Clock()
n = 0
strips[n].iter()
image = strips[n].next()


def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)
 
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type==KEYUP and e.key==K_RETURN:
            n+=1
            if n>=len(strips):
                n = 0
            strips[n].iter()
                  
    ticks = time.get_ticks() 
    if ticks > next_tick:
        next_tick += speed
        angle += 1
        coords = move_coords(angle, 2, coords)
        rect.topleft = coords
         
    screen.fill((0,0,30))
    screen.blit(image, (rect[0],rect[1]))
    display.flip()
    image = strips[n].next()
    clock.tick(FPS)
quit()
