from pygame import *
import math

class boomerang():
    def __init__(self,startcoordinates,angle,rect,speed,next_tick):
        self.angle, self.rect, self.speed, self.next_tick = angle, rect, speed, next_tick
        self.startcoordinates = (startcoordinates[0],startcoordinates[1])
    def move_coordinates(angle, radius, startcoordinates):
        self.theta = math.radians(angle)
        self.radius, self.startcoordinates = radius, startcoordinates
        return self.startcoordinates[0] + self.radius * math.cos(theta), self.startcoordinates[1] + self.radius * math.sin(theta)
    def ticks(self):
        self.ticks = time.get_ticks()
        if self.ticks>self.next_tick:
            self.next_tick+=self.speed
            self.angle+=1
            self.startcoordinates = self.move_coordinates(self.angle,2,self.startcoordinates)
            self.rect.topleft = self.startcoordinates

screen = display.set_mode((800, 600))
display.set_caption("Boomerang")
clock = time.Clock()

coords = 400, 200
angle = 0
rect = Rect(*coords,20,20)
speed = 1
next_tick = 500

boomerang = boomerang(coords,angle,rect,speed,next_tick)
 
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    boomerang.ticks()
##    ticks = time.get_ticks() 
##    if ticks > next_tick:
##        next_tick += speed
##        angle += 1
##        coords = move_coords(angle, 2, coords)
##        rect.topleft = coords
         
    screen.fill((0,0,30))
    screen.fill((0,150,0), boomerang.rect)
    display.flip()
    clock.tick(120)
quit()
