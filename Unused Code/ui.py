"""
Controls right now (proof of concept):
J/K to control money
Up/Down Arrows to control Hearts
Space to control Current Weapon
M to hide/show map
Click on the Gear button in the top right corner to make the popup menu appear
    --> only resume and quit are available currently
"""

from pygame import *
#from link import person
import os
from imageload import imageload
from shopp import shopclass
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
screen = display.set_mode((800,740))
screenx,screeny = screen.get_size()

class player(object):
    def __init__(self,speed=3):
        self.speed = speed
        self.playermovement = "None"
        self.movex = 0
        self.movey = 0
        self.playersprite = image.load("images/People/player.png").convert()
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
            self.playermovement = None

player = player()
player.rect.x,player.rect.y = 100,75

ui = screen.subsurface(Rect(0,0,screenx,screeny))

heart = image.load('images/UI/heart.png').convert()
heart.set_colorkey((0,0,0))

##rupee = image.load('images/UI/rupee.png').convert()
##rupee.set_colorkey((255,255,255))

gear = image.load('images/UI/settings.png').convert()
gear.set_colorkey((255,255,255))

gearhover = image.load('images/UI/settingshover.png').convert()
gearhover.set_colorkey((255,255,255))

Exit = image.load('images/UI/Exit.png').convert()
Exit.set_colorkey((255,255,255))

ExitHover = image.load('images/UI/ExitHover.png').convert()
ExitHover.set_colorkey((255,255,255))

Resume = image.load('images/UI/Resume.png').convert()
ResumeHover = image.load('images/UI/ResumeHover.png').convert()

sword = image.load('images/UI/sword.png').convert()
sword.set_colorkey((255,255,255))

boomerang = image.load('images/UI/boomerang.png').convert()
boomerang.set_colorkey((0,0,0))

bow = image.load('images/UI/bow.png').convert()
bow.set_colorkey((255,255,255))

mapimg = image.load('images/map1.png').convert()

minmap = transform.scale(mapimg,(200,205))
heart = transform.scale(heart,(20,20))
##rupee = transform.scale(rupee,(35,35))
gear = transform.scale(gear,(35,35))
gearhover = transform.scale(gearhover,(35,35))
Exit = transform.scale(Exit,(130,55))
ExitHover = transform.scale(ExitHover,(130,55))
##gearmask = mask.from_surface(gear)
Resume = transform.scale(Resume,(130,55))
ResumeHover = transform.scale(ResumeHover,(130,55))
sword = transform.scale(sword,(75,75))
boomerang = transform.scale(boomerang,(75,75))
bow = transform.scale(bow,(75,75))

ExitRect = Exit.get_rect()
ExitRect.center = screenx//2,395##screeny//2
ResumeRect = Resume.get_rect()
ResumeRect.center = screenx//2,325
SettingsMenuRect = Rect(0,0,150,298-10-ExitRect.bottomright[1]+ExitRect[1]-55-45+10)
SettingsMenuRect.midtop = screenx//2,298-10

done = False

def drawminmap():
    minmaprect = minmap.get_rect()
    draw.rect(ui,(255,215,0),(screenx-205,screeny-205,minmaprect[2]+5,minmaprect[3]))
    ui.blit(minmap,(screenx-200,screeny-200))
def updatehearts(heartstatus=3,distapart=20):
    x,y = 3,0
    if heartstatus>0:
        for pos in range(heartstatus):
            ui.blit(heart,(x+distapart*pos,y))
def settings():
    ui.blit(gear,(755,10))
    if gear_rect.collidepoint(mx,my):
        ui.blit(gearhover,(755,10))
def settingsmenu(menuwallpadding=5):
    """
    add code to pause game here
    """
    draw.rect(ui,(255,215,0),SettingsMenuRect)#(ResumeRect[0]-menuwallpadding,ResumeRect[1]-menuwallpadding,ExitRect.bottomright[0]-ResumeRect.topleft[0]+15+menuwallpadding,ExitRect.bottomright[1]-ResumeRect.topleft[1]+15+menuwallpadding))
    ui.blit(Resume,ResumeRect)
    if ResumeRect.collidepoint(mx,my):
        ui.blit(ResumeHover,ResumeRect)
    ui.blit(Exit,ExitRect)
    if ExitRect.collidepoint(mx,my):
        ui.blit(ExitHover,ExitRect)
        
settingsbool = False
hearts,maxhearts = 3,10
gear_rect = Rect(755,10,35,35)
minmaptoggle = 1

"""
screen size in this demo has been adjusted to 800x740
    --> before, it was 800x800
    --> changing resolution should be fine since most things are positioned
        relative to the screen size

Everything below this is the updated ui/shop code, NOT COUNTING:
from shop import shop
"""

Fairies,Keys = 0,0

def showammo():
    draw.rect(ui,(255,215,0),(0,screeny-100,55,80))
    draw.rect(ui,(100,100,100),(0,screeny-95,50,70))
    ui.blit(bomb,(5,screeny-90))
    ui.blit(arrow,(5,screeny-50))
    if bombtot:
        bombstock = shop.hylian.render('%i'% bombtot,False,(173,214,198))
        ui.blit(bombstock,(40,screeny-90))
    else:
        bombstock = shop.hylian.render('0',False,(173,214,198))
        ui.blit(bombstock,(40,screeny-90))        
    if arrowtot:
        arrowstock = shop.hylian.render('%i'% arrowtot,False,(173,214,198))
        ui.blit(arrowstock,(40,screeny-50))
    else:
        arrowstock = shop.hylian.render('0',False,(173,214,198))
        ui.blit(arrowstock,(40,screeny-50))
bomb = imageload("images/UI/bomb.png",0.1,False,(255,255,255))
arrow = imageload("images/UI/Arrow.png",0.175,False,(255,255,255))
bombtot,arrowtot = 0,0
shop = shopclass(screen)

rupee = imageload("images/UI/rupee.png",0.175,False,(255,255,255))
rupeecolon = shop.hylian.render(":",False,(205,255,0))

clock = time.Clock()
while not done:
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    for e in event.get():
        if e.type==QUIT or e.type==MOUSEBUTTONUP and ExitRect.collidepoint(mx,my) and settingsbool:
            done = True
        if e.type==MOUSEBUTTONUP:
            if ResumeRect.collidepoint(mx,my):
                settingsbool = False
            if gear_rect.collidepoint(mx,my):
                settingsbool = True
            if shop.ExitRect.collidepoint(mx,my):
                shop.ui.blit(shop.ExitHover,shop.ExitRect)
                shop.shopbool = False
            if shop.tabbool==1:
                for q in range(len(shop.Qs)):
                    if shop.Qs[q].collidepoint(mx,my):
                        if q%2!=0 and shop.cost+shop.QVals[q]<=shop.rupeenum and shop.QStock[q] and shop.held[q//2]+1<=shop.QStock[q]:
                            shop.cost+=shop.QVals[q]
                            shop.QStock[q]-=1
                            shop.OldQStock = q
                            shop.held[q//2]+=1
                            shop.amt[q//2] = shop.hylian.render('%i'% shop.held[q//2],False,(173,214,198))
                        elif q%2==0 and shop.cost-shop.QVals[q]<=shop.rupeenum and shop.cost-shop.QVals[q]>=0 and shop.held[q//2]-1>=0:
                            shop.cost-=shop.QVals[q]
                            shop.QStock[shop.OldQStock]+=1
                            shop.held[q//2]-=1
                            shop.amt[q//2] = shop.hylian.render('%i'% shop.held[q//2],False,(173,214,198))
                        print("Current Cost: $",shop.cost)
                        print("Stocks:",shop.held)
            if shop.tabbool==-1:
                for q in range(len(shop.itemQs)):
                    if shop.itemQs[q].collidepoint(mx,my):
                        if q%2!=0 and shop.cost+shop.itemQVals[q]<=shop.rupeenum and shop.itemQStock[q] and shop.itemheld[q//2]+1<=shop.itemQStock[q]:
                            shop.cost+=shop.itemQVals[q]
                            shop.itemQStock[q]-=1
                            shop.itemOldQStock = q
                            shop.itemheld[q//2]+=1
                            shop.amt[4+q//2] = shop.hylian.render('%i'% shop.itemheld[q//2],False,(173,214,198))
                        elif q%2==0 and shop.cost-shop.itemQVals[q]<=shop.rupeenum and shop.cost-shop.itemQVals[q]>=0 and shop.itemheld[q//2]-1>=0:
                            shop.cost-=shop.itemQVals[q]
                            shop.itemQStock[shop.itemOldQStock]+=1
                            shop.itemheld[q//2]-=1
                            shop.amt[4+q//2] = shop.hylian.render('%i'% shop.itemheld[q//2],False,(173,214,198))
                        print("Current Cost: $",shop.cost)
                        print("Stocks:",shop.held)
            if shop.buyrect.collidepoint(mx,my) and shop.cost<=shop.rupeenum and shop.cost!=0:
                shop.rupeenum-=shop.cost
                if hearts<maxhearts and shop.amt[4] and shop.itemheld[0]:
                    hearts+=shop.itemheld[0]
                if shop.amt[5] and shop.amt[5] and shop.itemheld[1]:
                    Fairies+=shop.itemheld[1]
                if shop.amt[6] and shop.amt[6] and shop.itemheld[2]:
                    shop.hasmap = True
                if shop.amt[7] and shop.amt[7] and shop.itemheld[3]:
                    Keys+=shop.itemheld[3]
                bombtot+=shop.held[0]
                arrowtot+=shop.held[2]
                shop.amt[0],shop.amt[1],shop.amt[2],shop.amt[4],shop.amt[5],shop.amt[6],shop.amt[7] = shop.amt0,shop.amt1,shop.amt2,shop.amt4,shop.amt5,shop.amt6,shop.amt7
                print("Spent $",shop.cost)
                shop.held,shop.itemheld,shop.cost = [0,0,0,0],[0,0,0,0],0
            if shop.toggleTabRect.collidepoint(mx,my):
                shop.tabbool*=-1
        if e.type==KEYUP:
            if e.key==K_UP and hearts<maxhearts:
                hearts+=1
            if e.key==K_DOWN and hearts>0:
                hearts-=1
            if e.key==K_j:
                shop.rupeenum+=1
            if e.key==K_k and shop.rupeenum>0:
                shop.rupeenum-=1
            if shop.ShopKeeperRect.colliderect(player.rect) and e.key==K_SPACE and not shop.shopbool:
                shop.shopbool = True
            if e.key==K_m and shop.hasmap:
                minmaptoggle*=-1
    if not shop.shopbool:
        player.keys()
    screen.fill((175,175,175))
    screen.blit(player.playersprite,(player.rect.x,player.rect.y))
    shop.settingsmenu(mx,my)
    if shop.shopbool:
        if shop.tabbool==1:
            ui.blit(shop.amt[0],shop.amt0rect)
            ui.blit(shop.amt[1],shop.amt1rect)
            ui.blit(shop.amt[2],shop.amt2rect)
        else:
            ui.blit(shop.amt[4],shop.amt4rect)
            ui.blit(shop.amt[5],shop.amt5rect)
            ui.blit(shop.amt[6],shop.amt6rect)
            ui.blit(shop.amt[7],shop.amt7rect)
    shop.rupeehandling()
    ui.blit(rupee,(0,25))
    ui.blit(rupeecolon,(35,32.5))
    settings()
    if settingsbool:
        settingsmenu()
    updatehearts(hearts)
    if minmaptoggle==1 and shop.hasmap:
        drawminmap()
    showammo()
    clock.tick(60)
    display.flip()
quit()
