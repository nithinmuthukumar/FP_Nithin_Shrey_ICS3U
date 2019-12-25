# pygameRev1.py
from pygame import *
import os
import pickle
from imageload import imageload

def drawAll(screen, level):
    screen.blit(back, (-800*2,-740*2))
    for x in range(SCREENX):
        for y in range(SCREENY):
            c = level[x][y]
            if c > 0:
                draw.rect(screen, col[c], (x*20, y*20, 20, 20))    

def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")        # load my board that I pickled
        return pickle.load(myPFile)       
    else:
        print("w")
        return [[0]*SCREENY for x in range(SCREENX)]
    

def saveMap(level, fname):
    myPFile = open(fname, "wb")
    pickle.dump(level, myPFile)
    myPFile.close()
        
size = width, height = 800, 740
screen = display.set_mode(size)
col = [(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
SCREENX = 40
SCREENY = 37

current = 1    # my current paint colour / contents
back = imageload("lostwoods.png",4,False)

level = loadMap("(2,2).txt")
print(len(level))
print(len(level[0]))
running = True
myClock = time.Clock()
while running:
    for evnt in event.get():                # checks all events that happen
        if evnt.type == QUIT:
            running = False
            
    keys = key.get_pressed()                # get numbers from KB
    for i in range(8):
        if keys[i+48]:
            current = i
        
    if keys[K_SPACE]:
        mx, my = mouse.get_pos()
        gx = mx // 20
        gy = my // 20
        level[gx][gy] = current
        draw.rect(screen, col[level[gx][gy]], (gx*20, gy*20, 17, 17))
    if keys[K_a]:
        mx, my = mouse.get_pos()
        gx = mx // 20
        gy = my // 20
        level[gx][gy] = 0
        draw.rect(screen, col[level[gx][gy]], (gx*20, gy*20, 17, 17))
        
    drawAll(screen, level)
    display.flip()

    myClock.tick(60)                        
    
quit()
saveMap(level, "(2,2).txt")

