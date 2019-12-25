# levelRun.py
from pygame import *
import pickle
import os
from imageload import imageload
def find(grid, val):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == val:
                return (x,y)
    return (-1,-1)


def drawAll(screen, guyX, guyY):
    screen.blit(back, (0,0))
    draw.circle(screen, (255,0,0), (guyX*20+10, guyY*20+10),8)
    display.flip()

def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")        # load my board that I pickled
        return pickle.load(myPFile)       
    else:
        return [[0]*SCREENY for x in range(SCREENX)]
        
size = width, height = 800, 800
screen = display.set_mode(size)

BLOCKED = 0
GRASS = 2
ROAD = 3
START = 4

SCREENX = 40
SCREENY = 40
guyX, guyY = 20, 20

current = 1
back = imageload("housebackground.png",3.5,False)

level = loadMap("housebackground.txt")
start = find(level,START)
if start != (-1,-1):
    guyX, guyY = start
    
running = True
myClock = time.Clock()
while running:
    for evnt in event.get():               
        if evnt.type == QUIT:
            running = False

    oldX, oldY = guyX, guyY
    keys = key.get_pressed()                # Basic arrows    
    if keys[K_LEFT]  : guyX -= 1
    if keys[K_RIGHT] : guyX += 1
    if keys[K_UP]    : guyY -= 1
    if keys[K_DOWN]  : guyY += 1

    if guyX<0 or guyX>=SCREENX or guyY<0 or guyY>=SCREENY or level[guyX][guyY] == BLOCKED:          # For now the only values in the grid that matter
        guyX, guyY = oldX, oldY 
    
    drawAll(screen, guyX, guyY)
    myClock.tick(20)                        
    
quit()

