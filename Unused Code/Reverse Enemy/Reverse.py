from pygame import *
import math, os
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"

class player(object):
    def __init__(self,speed=4):
        self.speed = speed
        self.playermovement = "None"
        self.movex = 0
        self.movey = 0
        self.playersprite = image.load("player.png").convert()
        self.playersprite.set_colorkey((255,255,255))
        self.playersprite = transform.scale(self.playersprite,(20,20))
        self.rect = self.playersprite.get_rect()
    def keys(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y-=self.speed
            self.playermovement = "Up"
        if keys[K_a]:
            self.rect.x-=self.speed
            self.playermovement = "Left"
        if keys[K_s]:
            self.rect.y+=self.speed
            self.playermovement = "Down"
        if keys[K_d]:
            self.rect.x+=self.speed
            self.playermovement = "Right"
        if not keys[K_w] and not keys[K_a] and not keys[K_s] and not keys[K_d]:
            self.playermovement = "None"

class Reverso():
    """
    Learn and use inheritance of player class
    """
    def __init__(self,speed=4):
        self.speed = speed
        self.movex = 0
        self.movey = 0
        self.reversosprite = image.load("reverso.png").convert()
        self.reversosprite.set_colorkey((255,255,255))
        self.reversosprite = transform.scale(self.reversosprite,(20,20))
        self.rect = self.reversosprite.get_rect()
    def keys(self):
        if screen.get_rect().collidepoint(self.rect.midleft):
            if player.playermovement == "Right":
                self.rect.x -= self.speed
        if screen.get_rect().collidepoint(self.rect.midright):
            if player.playermovement == "Left":
                self.rect.x += self.speed
        if screen.get_rect().collidepoint(self.rect.midbottom):
            if player.playermovement == "Up":
                self.rect.y += self.speed
        if screen.get_rect().collidepoint((self.rect.midtop[0],self.rect.y-self.speed)):
            if player.playermovement == "Down":
                self.rect.y -= self.speed
        
screen = display.set_mode((800,600))
display.set_caption("Reverso")
done = False

player = player()
player.rect.x = 20
player.rect.y = 20

reverso = Reverso()
reverso.rect.x = 400
reverso.rect.y = 400

clock = time.Clock()
while not done:
    for e in event.get():
        if e.type==QUIT:
            done = True
    changeintime = clock.tick(60)/1000.0
    player.keys()
    reverso.keys()
    screen.fill(0)
    screen.blit(player.playersprite, (player.rect.x, player.rect.y))
    screen.blit(reverso.reversosprite, (reverso.rect.x,reverso.rect.y))
    display.flip()
    oldx,oldy = player.rect.x,player.rect.y
quit()
