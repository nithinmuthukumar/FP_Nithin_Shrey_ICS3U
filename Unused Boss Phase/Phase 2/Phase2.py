from pygame import *
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import spritesheet
from sprite_strip_anim import SpriteStripAnim
from imageload import imageload

class player(object):
    def __init__(self,speed=4):
        self.speed = speed
        self.playermovement = "None"
        self.movex = 0
        self.movey = 0
        self.playersprite = imageload("player.png",0.1,False,(255,255,255))
        self.rect = self.playersprite.get_rect()
    def keys(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>0:
            self.rect.y-=self.speed
            self.playermovement = "Up"
        if keys[K_a] and self.rect.x>0:
            self.rect.x-=self.speed
            self.playermovement = "Left"
        if keys[K_s] and self.rect.bottom<600:
            self.rect.y+=self.speed
            self.playermovement = "Down"
        if keys[K_d] and self.rect.right<800:
            self.rect.x+=self.speed
            self.playermovement = "Right"
        if not keys[K_w] and not keys[K_a] and not keys[K_s] and not keys[K_d]:
            self.playermovement = "None"

player = player()
player.rect.x,oldx = 20,20
player.rect.y,oldy = 20,20

screen = display.set_mode((800,740))
BG = imageload("images/Coliseum.png",1,False,(255,255,255))
clock = time.Clock()

class bullsentry():
    """
    Used spritesheet iterator from
    https://www.pygame.org/wiki/Spritesheet
    Variables:
    warn = timer for how long the warning crosshair is displayed
    pos2 = the position that the bomb is dropped on
    shot = whether the bomb has been shot out or not
    explode = whether the bomb has landed or not
    hit = whether the bomb hit the player
          --> used to make sure player is only registered to be hit once.
    rise = when the minotaur is levitating and can shoot
    down = when the minotaur is resting and not levitating
    turn = keeps track of how long the minotaur levitates
    godown = makes sure that the minotaur slowly goes back down when he stops levitating
    n = keeps track of which spritesheet to animate through/next
    strips = list of all spritesheets relating to the 'bomb'
    pulse = the current spritesheet
    """
    def __init__(self):
        self.n,self.strips = 0,[
    SpriteStripAnim('images/FFAnim.png', (0,0,64,64),8,(0,0,0),True,3) +
    SpriteStripAnim('images/FFAnim.png', (64,64,64,64),8,(0,0,0),True,3),
    SpriteStripAnim('images/Explode.bmp', (0,0,24,24),8,1,True,5)
]
        self.goup = imageload("images/RiseUp.png",1,False,(255,255,255))
        self.godown = imageload("images/GoDown.png",1,False,(255,255,255))
        self.gouprect = self.goup.get_rect()
        self.godownrect = self.godown.get_rect()
        self.gouprect.center = (screen.get_rect().centerx,278)#screen.get_rect().centery-25)
        self.godownrect.center = (screen.get_rect().centerx,screen.get_rect().centery)
        self.strips[self.n].iter()
        self.warn = 0
        self.turn = 0
        self.pos2 = False
        self.shot = False
        self.explode = False
        self.hit = False
        self.rise = False
        self.down = True
        self.godownbool = False
    def update(self,p,time):
        self.warn+=time
        self.turn+=time
        if not self.rise and self.down:
            if not self.godownbool and self.warn>1000:
                self.rise = True
                self.down = False
                self.godownbool = True
                self.warn = 0
                self.turn = 0
            elif self.godownbool and self.warn>3000:
                self.godownbool = False
                self.warn = 0
            if not self.godownbool:
                self.godownrect[1] = self.godownrect[1]-self.warn//250     #sometimes the bull goes higher/lower by a pixel or 2, because of how many ticks pass between the if statement and what happens in the if statement
            elif self.godownbool and self.godownrect.centery<screen.get_rect().centery:
                self.godownrect[1] = self.godownrect[1]+self.warn//250
##            print("Current Minotaur Y Coordinate:",self.godownrect[1])
            screen.blit(self.godown,self.godownrect)
        if self.rise:
            screen.blit(self.goup,self.gouprect)
            if not self.shot:
                if not self.pos2:
                    self.pos2 = p.rect.x,p.rect.y
                elif self.pos2:
                    if not self.explode:
                        screen.blit(pulse,(self.pos2[0]-20,self.pos2[1]-24))
                    elif self.explode and self.turn>2015:       #2015 covers the problem that the explode sometimes blits after the minotaur jumps up
                        screen.blit(pulse,(self.pos2[0],self.pos2[1]))
                if self.warn > 1500 and not self.explode:
                    self.n += 1
                    if self.n >= len(self.strips):
                        self.n = 0
                    self.strips[self.n].iter()
                    self.explode = True
                if self.explode and self.pos2[0]>=p.rect.x-10 and self.pos2[0]<=p.rect.x+10 and self.pos2[1]>=p.rect.y-10 and self.pos2[1]<=p.rect.y+10 and not self.hit:
                    """
                    add code to take away link's health here
                    No need to worry about more than one hit being taken
                    """
                    print("Hit")
                    self.hit = True
                if self.warn > 2000:
                    self.n += 1
                    print(self.n)
                    if self.n >= len(self.strips):
                        self.n = 0
                    self.strips[self.n].iter()
                    self.warn,self.shot,self.explode = 0,True,True
            if self.shot:
                if self.warn > 750:
                    self.pos2,self.shot,self.explode,self.hit,self.warn = False,False,False,False,0
##            print(self.turn)
            if self.turn>2750*3+2:#2750*3:#9450:#8635:#9450:
##                print(True)
                self.warn,self.turn = 0,0
                self.rise = False
                self.down = True
                self.godownbool = True
b = bullsentry()
pulse = b.strips[b.n].next()

done = False
while not done:
    for e in event.get():
        if e.type==QUIT:
            done = True
        if e.type==KEYUP:
            if e.key==K_RETURN:
                b.n += 1
                if b.n >= len(b.strips):
                    b.n = 0
                b.strips[n].iter()
    player.keys()
    screen.fill((0,0,0))##    screen.blit(BG,(0,0)) -- if you uncomment this,
                        ##    change clock.tick(60) to clock.tick(120)
    b.update(player,clock.get_time())
    screen.blit(player.playersprite, (player.rect.x, player.rect.y))
    clock.tick(60)##    clock.tick(120)
    display.flip()
    pulse = b.strips[b.n].next()
quit()
