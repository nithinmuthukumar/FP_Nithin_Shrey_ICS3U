from pygame import *
import math
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
screen = display.set_mode((800,600))
display.set_caption("Player Move")
done = False

class player(object):
    def __init__(self):
        self.movex = 0
        self.movey = 0
        self.playersprite = image.load("player.png")
        self.playersprite.set_colorkey((255,255,255))
        self.playersprite = transform.scale(self.playersprite,(20,20))
        self.rect = self.playersprite.get_rect()
    def keys(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y-=3
        if keys[K_a]:
            self.rect.x-=3
        if keys[K_s]:
            self.rect.y+=3
        if keys[K_d]:
            self.rect.x+=3

class enemy(object):
    def __init__(self,sprite,startx,starty,speed=2):
        self.sprite = sprite
        #lets user decide where to place sprite
        self.rect = self.sprite.get_rect( center = (startx,starty))
        #if no speed is passed, the default is 2 -- change to 3 to make it look smoother
        #changing to 3 still makes it have issues (enemy will get stuck on link if link moves in a certain direction
        #these issues can be solved by tweaking the changeintime variable
        self.speed = speed
    def approach(self,player):
        #distance formula between player and enemy
        distformula = math.sqrt((player.x - self.rect.x)**2 + (player.y - self.rect.y)**2)
        if distformula!=0 and distformula!=0:
            x = (player.x - self.rect.x) / distformula
            y = (player.y - self.rect.y) / distformula
            return (x,y)
    def update(self,player):
        pos2 = self.approach(player)
        if pos2:    #if approach doesnt return False -- no 0
            self.rect.x += pos2[0] * self.speed     #change in x
            self.rect.y += pos2[1] * self.speed     #change in y

#creates the player instance
player = player()
player.rect.x = 20
player.rect.y = 20

#creates the enemy instance
enemysprite = image.load('enemy.png').convert()
enemysprite.set_colorkey((255,255,255))
enemysprite = transform.scale(enemysprite,(20,20))
enemy1 = enemy(enemysprite,700,500)

enemysprite2 = image.load('enemy2.png').convert()
enemysprite2.set_colorkey((255,255,255))
enemysprite2 = transform.scale(enemysprite2,(20,20))
enemy2 = enemy(enemysprite2,200,500)

clock = time.Clock()
while not done:
    for e in event.get():
        if e.type==QUIT:
            done = True
    player.keys()
    screen.fill(0)
    changeintime = clock.tick(60)/1000.0    #this took me too long to figure out to use
    enemy1.update(player.rect)
    enemy2.update(player.rect)
    screen.blit(player.playersprite,(player.rect.x,player.rect.y))
    screen.blit(enemy1.sprite,(enemy1.rect.x,enemy1.rect.y))
    screen.blit(enemy2.sprite,(enemy2.rect.x,enemy2.rect.y))
    display.flip()
quit()
