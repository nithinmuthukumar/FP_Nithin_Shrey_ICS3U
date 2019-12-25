from pygame import*
import datetime
from math import*
from random import*
from glob import*
import pickle
from imageload import imageload
import os

page="game"
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
screen=display.set_mode(((800,740)),DOUBLEBUF|HWSURFACE)

#for 2d list mask, 1 is walkable 4 is start and 0 is boundary, and 6 is scroll
#create sprite groups
itemsprites=sprite.Group()
allsprites=sprite.Group()
enemysprites=sprite.Group()
weaponsprites=sprite.Group()
mainsprite=sprite.Group()
offscreenenemies=sprite.Group()
wizzrobesprites=sprite.Group()
enemyweaponsprites=sprite.Group()
offscreenweapons=sprite.Group()
deadsprites=sprite.Group()
sentrybullets=sprite.Group()
hadiesprites=sprite.Group()


class gameobj(sprite.Sprite):
    def __init__(self,sprites,x,y,speed,move):
        sprite.Sprite.__init__(self)#initializes sprites
        self.movement=move
        self.frame=0#frame in animation
        self.ani=sprites#dictionary of images
        self.x=x
        self.y=y
        self.speed=speed
        self.direction="left"#if statement for direction
        self.image=self.ani[self.movement][self.frame]
        
        self.rect=self.image.get_rect(center=(self.x,self.y))#modify when starting point is known
 #       self.state="normal"#link states can be : hurt,defend,normal and attack #hurt so buffer between next collide, defend so he cant be hurt and attack where he is the one who is hurting, and normal is vulnerable
    def animate(self):
        
        if self.frame>len(self.ani[self.movement]):
            self.frame=0
        if self.frame!=len(self.ani[self.movement]):#looping through animations

            self.image=(self.ani[self.movement][self.frame])
            self.rect=self.image.get_rect(center=(self.x,self.y))
            
            self.frame+=1
           
        else:
            self.frame=0
    def move(self):
        global mask
        if self.direction=="left" and self.bound():
            self.x-=self.speed
            return True
            
        elif self.direction=="right" and self.bound():
            self.x+=self.speed
            return True
   
        elif self.direction=="up" and self.bound():
            self.y-=self.speed
            return True
        
        elif self.direction=="down" and self.bound():
            self.y+=self.speed
            return True
    def checkcollide(self,group):
        if self in allsprites:
            
            if sprite.spritecollide(self,group,False):
                for i in (sprite.spritecollide(self,group,False)):
                    
         
                                          
                    i.hurt()
                return True
            else:
                return False
class sentrybullet(sprite.Sprite):
    def __init__(self,startx,starty,rng,location,speed=4,homing=False):
        sprite.Sprite.__init__(self)
        self.spawnspot =startx,starty
        self.homing = homing
        self.speed=speed
        self.x,self.y=startx,starty
        self.location=location
    
        if not self.homing:
            self.image = image.load("images/sentry/splodebullet.png").convert()
            self.image.set_colorkey((0,0,0))
            self.image = transform.scale(self.image,(20,20))
        else:
            self.image = image.load("images/sentry/splodebullethoming.png").convert()
            self.image.set_colorkey((255,255,255))
            self.image = transform.scale(self.image,(20,20))
        self.range = Rect(self.spawnspot[0]-rng,self.spawnspot[1]-rng,rng*2,rng*2)
        self.pos2 = 0
        self.reload = 0
        self.rect = self.image.get_rect( center = (self.x,self.y))
        if self.homing:self.speed = speed
        if not self.homing:self.speed = speed+3
        sentrybullets.add(self)
    def distance(self):
        self.increment=link.x-self.x
        self.increment=link.y-self.y
    def approach(self):
        x_dist = link.x - self.rect.x
        y_dist = link.y - self.rect.y
        return atan2(-y_dist, x_dist) % (2 * pi)
    def work(self,time):
        self.reload += time
        if self.range.contains(link.rect) and self.reload<2 and self.checkcollide(mainsprite)==False and self.location==(backx,backy): #homing bullets only last 2 seconds:
            
            allsprites.add(self)
 
            if self.homing:
                self.pos2 = self.approach()
               
            elif not self.homing and not self.pos2:
                distformula = sqrt((link.x - self.rect.x)**2 + (link.y - self.rect.y)**2)
                if distformula!=0:
                    self.rect.x+= ((link.x - self.rect.x) / distformula)*self.speed#enemy needs a speed attribute
                    self.rect.y+= ((link.y - self.rect.y) / distformula)*self.speed

            if self.pos2 and self.range.contains(self.rect) and self.homing:
              #if approach doesnt return False -- no 0
                self.rect.x += (cos(self.pos2) * self.speed)     #change in x
                self.rect.y -= (sin(self.pos2) * self.speed)     #change in y
        
            
         
        else:
            self.reset()
 
    def reset(self):
        
        self.reload=0
        self.rect.x=self.spawnspot[0]
        self.rect.y=self.spawnspot[1]
        allsprites.remove(self)
    def checkcollide(self,group):
        if self in allsprites:
            
            if sprite.spritecollide(self,group,False):
                for i in (sprite.spritecollide(self,group,False)):
                    i.hurt()
                    return True
        
        return False
            
            
class item(sprite.Sprite):
    def __init__(self,image,effect):
        sprite.Sprite.__init__(self)
        self.x,self.y=0,0
        self.image=image[0]
        self.rect=Rect((self.x,self.y,self.image.get_width(),self.image.get_height()))
        self.effect=effect
    def appear(self,x,y):
        self.rect=Rect((x,y,self.image.get_width(),self.image.get_height()))
        allsprites.add(self)
    def hurt(self):
        allsprites.remove(self)
        if self.effect=="rupeenum+=1":
            global rupeenum
            rupeenum+=1
            self.rect.x-=90000
        if self.effect=="link.health+=1":
            link.health+=1
            self.rect.x-=900000 
        blitback(backx,backy)
    
class zelda(gameobj):
    def __init__(self,sprites,speed,health,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        mainsprite.add(self)
        self.inispeed=self.speed
        self.health=health
        self.maxhealth=20
        self.state="normal"
        allsprites.add(self)
        self.slashing=False
        self.rolling=False
    def walk(self,keys):
        
            
        if keys[K_LEFT] or keys[K_a]:
            if link.rolling:
                link.rolling=False
            link.direction="left"
            link.movement="walkleft"
            link.animate()
            
            link.move()
        
        if keys[K_RIGHT] or keys[K_d]:
            if link.rolling:
                link.rolling=False
            link.direction="right"
            link.movement="walkright"
            link.animate()
            link.move()
            
        if keys[K_UP] or keys[K_w]:
            if link.rolling:
                link.rolling=False
            link.direction="up"
            link.movement="walkup"
            link.animate()
            link.move()
            
        if keys[K_DOWN] or keys[K_s]:
            if link.rolling:
                link.rolling=False
            link.direction="down"
            link.movement="walkdown"
            link.animate()
            link.move()
    def roll(self):
       
 
        self.movement="roll"+self.direction
        self.speed+=1
        self.animate()
        self.move()
    
    
        if len(self.ani[self.movement])==self.frame:
            

            self.rolling=False
     
            self.movement="walk"+self.direction
            self.frame=0
            self.speed=self.inispeed
     
    def slash(self):
        self.movement="slash"+self.direction
        self.state="attack"
        self.animate()
        if len(self.ani[self.movement])==self.frame:
            self.slashing=False
            self.frame=0
            self.state="normal"
            self.animate()
    
            
        
    def hurt(self):
        self.state="hurt"
 
        self.health-=1
        blitback(backx,backy)
 
        if self.health==0:
            self.movement="death"
            self.animate()
            time.wait(200)
 #           self.kill()
   
       
    def bound(self):#makes sure that player stays in boundaries
        global backx,backy,visback,lostwoodsmask,floorbound
        if self.direction=="right":
            if (link.x+link.image.get_width())//20>39:
                backx+=1
                self.x-=800
                blitback(backx,backy)
            elif floorbound[(self.x)//20+1][self.y//20]==1:
                return False
              
        if self.direction=="left":
            if (self.x-5//20)<0 :
                backx-=1
                self.x+=800
                blitback(backx,backy)
            elif floorbound[(self.x)//20-1][self.y//20]==1:              
                return False
          
        if self.direction=="up":
            if link.y//20<0 :
                
                backy-=1
                self.y+=740
                blitback(backx,backy)
            elif floorbound[(self.x)//20][(self.y)//20-1]==1:
                return False
        if link.direction=="down":
            if (self.y+self.image.get_height())//20>36 :
                backy+=1
                self.y-=740
                blitback(backx,backy)
            elif floorbound[(self.x)//20][self.y//20+1]==1:
                return False
     
        return True

class enemy(gameobj):
    def __init__(self,sprites,speed,health,location,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        self.startpos=(x,y)
        self.health=health
        self.add(enemysprites)
        self.location=location
        self.hurttime=0
        self.state="normal"
        offscreenenemies.add(self)


    def pathfind(self):#self is enemy
        ################################# nithin logic
        global floorbound
        
        floor=floorbound
        linkx,linky=link.x//20,link.y//20
        
        enemyx,enemyy=self.x//20,self.y//20
        start=(enemyx,enemyy)
        end=(linkx,linky)
        
        def heuristic(linkx,linky,x,y):
            dist1=sqrt((x-linkx)**2+(y-linky)**2)
            dist2=abs(x-linkx)+abs(y-linky)
            dist=(dist2+dist1)/2
            
            return int(dist*10)
        def dirs(i,d,floor=False):
            if floor:
                return floor[i[0]+d[0]][i[1]+d[1]]
            else:
                return (i[0]+d[0],i[1]+d[1])
        currscore=dict()               
        current=[]
        directions=[(1, 0), (0, 1), (0, -1), (-1, 0)]
        open_list=[]
        
        if (enemyx,enemyy)!=(linkx,linky):
            for d in directions:
                if dirs(start,d,floor)==0:
                    open_list.append(dirs(start,d))
            for c in open_list:
                currscore[c]=(heuristic(linkx,linky,c[0],c[1]))
            nextpos=(min(currscore, key=currscore.get))

            if nextpos[0]+1==enemyx:
                self.movement="left"

                
            if nextpos[0]-1==enemyx:
                self.movement="right"

                
            if nextpos[1]-1==enemyy:
                self.movement="down"
      
                
            if nextpos[1]+1==enemyy:
                self.movement="up"
    
            self.move()
            self.direction=self.movement
 
                                                                          
    def hurt(self):
        self.hurttime+=1
       
        self.state="hurt"
        if self.hurttime<4:
            pass
        else:
            self.health-=1
            self.hurttime=0
            self.state="normal"
        if self.health==0:
            self.kill()
            deadsprites.add(self)
            self.itemdrop()
  
        
    def itemdrop(self):
         itemdrop=choice(["rupee","heart"])
         dropchance=[1,1,1,1,1,1]
         if choice(dropchance)==1:
             if itemdrop=="rupee":
                 grupee=item(greenrupee,"rupeenum+=1")
                 itemsprites.add(grupee)
                 grupee.appear(self.x,self.y)
             if itemdrop=="heart":
                 heartt=item(heartups,"link.health+=1")
                 itemsprites.add(heartt)
                 heartt.appear(self.x,self.y)
    def bound(self):#makes sure that player stays in boundaries
        return True
             
class wizzrob(enemy):
    def __init__(self,sprites,speed,health,x,y,location,atk,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        wizzrobesprites.add(self)
        self.atk=atk
        self.attacking=False
        
    def turn(self):
        diffx=link.x-self.x
        diffy=link.y-self.y
        change=False
        if self.attacking!=True:
            if abs(diffx)<abs(diffy):
                if diffy>0:
                    if self.direction!="down":
                            self.direction="down"
                            self.movement="down"
                            change=True
                else:
                    if self.direction!="up":
                            self.direction="up"
                            self.movement="up"
                            change=True
            else:
                if diffx<0:
                    if self.direction!="left":
                        self.direction="left"
                        self.movement="left"
                        change=True
                else:
                    if self.direction!="right":
                        self.direction="right"
                        self.movement="right"
                        change=True
            if change:
                self.frame=-1
            self.animate()
 
        self.attack()
        
            
    def disappear(self):
        teleport=(self.x//20,self.y//20)
        if sqrt((self.x-link.x)**2+(self.y-link.y)**2)<100:#if their very close disappear
          
            while floorbound[teleport[0]][teleport[1]]==1 or sqrt((teleport[0]-self.x//20)**2+(teleport[1]-self.y//20)**2)<5:
                teleport=(randint(0,39),randint(0,36))
            self.x=teleport[0]*20
            self.y=teleport[1]*20

            
    def attack(self):
        global backx,backy
        if self.location==(backx,backy):
            if self.frame==len(self.ani[self.movement]) and self.attacking!=True:
                
                self.attacking=True
                allsprites.add(self.atk)
                self.atk.rect.x,self.atk.rect.y=self.x,self.y
            x_dist = link.x - self.atk.rect.x
            y_dist = link.y - self.atk.rect.y
            atkmove=atan2(y_dist, x_dist) % (2 * pi)
            self.atk.rect.x+=int(cos(atkmove) * self.speed)
            self.atk.rect.y+=int(sin(atkmove) * self.speed)
            if link.state=="normal":
                if self.atk.checkcollide(mainsprite):
                    self.attacking=False
        else:
            allsprites.remove(self.atk)
            self.attacking=False
            
                
    def operate(self):
            self.turn()
            self.disappear()
class hadi(enemy):
    def __init__(self,sprites,speed,health,location,x,y,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        hadiesprites.add(self)
        self.rng=10
        self.active=False
    def detect(self):
        if self.active==False:
            if sqrt((self.x-link.x)**2+(self.y-link.y)**2)<100:
                self.movement="wakeup"
                self.animate()
        
        if self.movement=="wakeup" and len(self.ani[self.movement])==self.frame:
            self.movement="down"
            self.active=True
        if self.active:
            
            self.pathfind()
            if self.health<3:
                self.movement="shelldown"
            self.animate()
     
        
            
            
            
        
                
            
    
        
class weapon(gameobj):
    def __init__(self,sprites,speed,limit,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        self.equipped=False
        self.appear=False
        self.limit=limit
        self.shoot=False
        self.vx,self.vy=5,3
        weaponsprites.add(self)
    def reset(self):
        self.remove(wallsprites)
    def bound(self):
        return True
def boomer(angle,increment):
    if keys[K_j] and boomerang.shoot!=True:
        allsprites.add(boomerang)
        link.movement="boomerang"+link.direction
        for i in range(2):
            link.animate()
            display.update()
        boomerang.shoot=True
        boomerang.x,boomerang.y=link.x,link.y
    if boomerang.shoot==True:
        boomerang.animate()
        theta = radians(angle)
        boomerang.x,boomerang.y=link.x + increment * cos(theta), link.y+ increment* sin(theta)
    if boomerang.shoot==False:
        allsprites.remove(boomerang)
def bombthrow():
    if keys[K_k] and bomb.shoot==True:
        allsprites.add(bomb)
        link.movement="bomb"+link.direction
        for i in range(2):
            link.animate()
            display.update()
        bomb.shoot=True
        bomb.x,bomb.y=link.x,link.y
    if bomb.shoot==True:
        if bombtimer<3000:
            if link.direction=="up" and bomb.rect.y-self.speed>self.totalpos[1]-self.dist and self.rect.y-self.speed>0:
                bomb.y-=bomb.speed
            if link.direction=="down":
                bomb.y+=bomb.speed
       
            if link.direction=="left":#and self.rect.x-self.speed>self.totalpos[0]-self.dist and self.rect.x-self.speed>0 and self.bombmove:
                self.vy+=0.05
                self.rect.x-=self.vx
                self.rect.y+=self.vy
                if self.rect.y>self.totalpos[1]:
                    self.bombmove,self.explode = False,False
                self.explode = False
            if link.direction=="right":#and self.rect.x+self.speed<self.totalpos[0]+self.dist and self.rect.x+self.speed<800 and self.bombmove:
                self.vy+=0.05
                self.rect.x+=self.vx
                self.rect.y+=self.vy
                
        
        
    
def arrowshoot():
    global arrowcounter
    if keys[K_l] and arrow.shoot!=True:

        link.movement="bow"+link.direction
        arrowcounter+=1
        link.animate()
        if arrowcounter==len(link.ani[link.movement]):
            arrow.direction=link.direction
            arrow.movement="arrow"+link.direction
            arrow.shoot=True
            arrow.x,arrow.y=link.x,link.y
            arrow.startx,arrow.starty=arrow.x,arrow.y
            arrow.animate()
            allsprites.add(arrow)
            arrowcounter=0       
    if arrow.shoot:
        arrow.move()
        arrow.animate()
        if arrow.direction=="left":
            if arrow.startx-arrow.limit>arrow.x:
                allsprites.remove(arrow)
                arrow.shoot=False

        if arrow.direction=="right":
            if arrow.startx+arrow.limit<arrow.x:
                allsprites.remove(arrow)
                arrow.shoot=False

        if arrow.direction=="up":
            if arrow.starty-arrow.limit>arrow.y:
                allsprites.remove(arrow)
                arrow.shoot=False
               
        if arrow.direction=="down":
            if arrow.starty+arrow.limit<arrow.y:
                allsprites.remove(arrow)
  
                arrow.shoot=False
    
            
            


    

def blitback(backx,backy):
    
    global mx,my
    global floorbound
    global minmaptoggle
    screen.blit(visback,(-800*backx,-740*backy))
    floorbound=housemask[backx][backy]
    if minmaptoggle==1:
        drawminmap()
    settings()
    updatehearts()
    rupeehandling()  
    drawcurrentitem()
        
    


    
def check2dlist():
    for x in range(len(floormap)):
        for y in range(len(floormap[x])):
            if floormap[x][y]==0:
                draw.rect(screen,(255,255,255),(x*20,y*20,20,20))


    

def loadMap(fname):#sirs 2d list modded
    lis=[]
    for i in fname:
        
        myPFile = open(i, "rb")        # load my board that I pickled
        lis.append(pickle.load(myPFile))
    return lis
    

def drawall(backx,backy):
    settings()
    try:
        allsprites.clear(screen,visback.subsurface(800*backx,740*backy,800,740))#did something weird when the background was not blit
    except:
        screen.blit(visback,(800*backx+link.x,740*backy+link.y))
    allsprites.update()
    allsprites.draw(screen)
 
    display.flip()    
        
       
#ui
screenx,screeny = screen.get_size()

font.init()
hylian = font.Font('ReturnofGanon.ttf', 35)
rupeenum = 0
rupeescolon = hylian.render(':',False,(205,0,0))



ui = screen.subsurface(Rect(0,0,screenx,screeny))
heart = image.load('heart.png').convert()
heart.set_colorkey((0,0,0))
rupee = image.load('rupee.png').convert()
rupee.set_colorkey((255,255,255))
gear = image.load('settings.png').convert()
gear.set_colorkey((255,255,255))
gearhover = image.load('settingshover.png').convert()
gearhover.set_colorkey((255,255,255))
Exit = image.load('Exit.png').convert()
Exit.set_colorkey((255,255,255))

ExitHover = image.load('ExitHover.png').convert()
ExitHover.set_colorkey((255,255,255))

Resume = image.load('Resume.png').convert()
ResumeHover = image.load('ResumeHover.png').convert()

sword = image.load('sword.png').convert()
sword.set_colorkey((255,255,255))

boomerang = image.load('boomerang.png').convert()
boomerang.set_colorkey((0,0,0))

bow = image.load('bow.png').convert()
bow.set_colorkey((255,255,255))

mapimg = image.load('map1.png').convert()

minmap = transform.scale(mapimg,(200,205))
heart = transform.scale(heart,(20,20))
rupee = transform.scale(rupee,(35,35))
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


        
mx,my=0,0
def drawminmap():
    minmaprect = minmap.get_rect()
    draw.rect(ui,(255,215,0),(screenx-205,screeny-205,minmaprect[2]+5,minmaprect[3]))
    ui.blit(minmap,(screenx-200,screeny-200))
def updatehearts(distapart=20):
    x,y = 3,0
    if link.health>0:
        for pos in range(link.health):
            ui.blit(heart,(x+distapart*pos,y))
def drawcurrentitem():
    weapons = [sword,boomerang,bow]
    draw.rect(ui,(255,215,0),(-5,665,80,80),3)
    ui.blit(weapons[curitemcounter],(0,665))
def rupeehandling():
    ui.blit(rupee,(-5,25))
    rupees = hylian.render('%i'% rupeenum,False,(205,255,0))
    ui.blit(rupeescolon,(30,24))
    ui.blit(rupees,(45,27))
def settings():
    global mx
    global my
    global page
    ui.blit(gear,(755,10))
    if gear_rect.collidepoint(mx,my):
        ui.blit(gearhover,(755,10))
        if mb[0]==1:
            page="settings"
            
def settingsmenu(menuwallpadding=5):
    global page
    global backx,backy
    """
    add code to pause game here
    """
    draw.rect(ui,(255,215,0),SettingsMenuRect)#(ResumeRect[0]-menuwallpadding,ResumeRect[1]-menuwallpadding,ExitRect.bottomright[0]-ResumeRect.topleft[0]+15+menuwallpadding,ExitRect.bottomright[1]-ResumeRect.topleft[1]+15+menuwallpadding))
    ui.blit(Resume,ResumeRect)
    
    if ResumeRect.collidepoint(mx,my):
        ui.blit(ResumeHover,ResumeRect)
        if mb[0]==1:
            page="game"
            
            blitback(backx,backy)
            return 
    ui.blit(Exit,ExitRect)
    if ExitRect.collidepoint(mx,my):
        ui.blit(ExitHover,ExitRect)
        if mb[0]==1:
            
            import menu
####################################################################################################################################################       
        

#all backgrounds #all 2dlist floors are 40*40
#background main var is visback

backx,backy=0,0
floors=imageload(glob("images/maps/*.png"),4,True)

housemask=[loadMap(glob("housemask/(0,*.txt")),loadMap(glob("housemask/(1,*).txt")),
           loadMap(glob("housemask/(2,*).txt")),loadMap(glob("housemask/(3,*).txt")),
           loadMap(glob("housemask/(4,*).txt")),loadMap(glob("housemask/(5,*).txt"))]
lostwoodsmask=[loadMap(glob("housemask/(0,*.txt")),loadMap(glob("housemask/(1,*).txt")),
           loadMap(glob("housemask/(2,*).txt")),loadMap(glob("housemask/(3,*).txt")),
           loadMap(glob("housemask/(4,*).txt")),loadMap(glob("housemask/(5,*).txt"))]
visback=floors[1]

floorbound=housemask[backx][backy]



#rupees
greenrupee=[imageload(("images/rupees/GreenRupee.png"),0.02)]#glob all rupees
heartups=[imageload(("heart.png"),0.05)]






dirnames=["left","right","up","down"]
linkanimations={k.split("/")[3]:imageload(glob(k+"/*.png"),2,True) for i in glob("images/link/*") for k in glob(i+"/*") }
sluganimations={k.split("/")[2]:imageload(glob(k+"/*.png"),2,True) for k in glob("images/slug/*") }
squidanimations={j:imageload(glob(k+"/*.png"),2,True) for k in glob("images/squid") for j in dirnames}
chuchuanimations={j:imageload(glob(k+"/*.png"),1,True) for k in glob("images/chuchu") for j in dirnames}
wizzrobeanimations={k.split("/")[2]:imageload(glob(k+"/*.png"),2,True) for k in glob("images/wizzrobe/*") }
wizzrobeweaponanimations={"fire":[imageload("images/weapons/wizzrobeweapon/wizzrobeweapon0.png",2)]}
boomeranganimations={"boomer":imageload(glob("images/weapons/boomerang/*.png"),2,True,(0,0,0))}
bombanimations={"bomb":imageload(glob("images/weapons/bomb/*.png"),2,True,(0,0,0))}
arrowanimations={"arrowup":[imageload("images/weapons/arrow/arrowup.png",0.5,(41,253,47))],
                 "arrowdown":[imageload("images/weapons/arrow/arrowdown.png",0.5,(41,253,47))],
                 "arrowleft":[imageload("images/weapons/arrow/arrowleft.png",0.5,(41,253,47))],
                 "arrowright":[imageload("images/weapons/arrow/arrowright.png",0.5,(41,253,47))]}
hadieanimations={k.split("/")[2]:imageload(glob(k+"/*.png"),3.7,True) for k in glob("images/hadienemy/*") }


#creating class objects
link=zelda(linkanimations,5,10,360,330,"walkleft")
hadie=hadi(hadieanimations,1,5,(4,0),200,300,"wakeup")
boomerang=weapon(boomeranganimations,10,200,link.x,link.y,"boomer")
arrow=weapon(arrowanimations,10,200,link.x,link.y,"arrowup")

wizzflame=weapon(wizzrobeweaponanimations,6,100,0,0,"fire")
enemyweaponsprites.add(wizzflame)
   
#enemies #going to create enemy spawner from file io later and implement like item creation
#need to replace with for loop
slug=enemy(sluganimations,5,2,(0,0),300,340,"left")
slug1=enemy(sluganimations,5,1,(1,0),200,340,"left")
slug2=enemy(sluganimations,5,1,(1,0),300,360,"left")
squid1=enemy(squidanimations,5,1,(0,0),150,400,"left")
chuchu=enemy(chuchuanimations,5,2,(2,0),150,400,"left")
wizzrobe=wizzrob(wizzrobeanimations,5,10,160,400,(2,0),wizzflame,"left")


#self,startx,starty,rng,location,speed=4,homing=False
regbullet = sentrybullet(50,50,700,(2,0),7)
homingbullet = sentrybullet(50,50,700,(2,0),7,True)


angle=20#angle of boomerang
increment=1#for boomerang radius
#clock object
clock=time.Clock()

#animation counter for enemies
anicounter=0#controls speed of animation

rupeenum=0
settingsbool = False
hearts,maxhearts = 3,10
curitemcounter = 0
gear_rect = Rect(755,10,35,35)
minmaptoggle = -1
hurttime=0

arrowcounter=0


blitback(backx,backy)#blit the background
key.set_repeat(1,500)

running=True
while running:
 
    
    keys=key.get_pressed()
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    clock.tick(60)

    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type==KEYDOWN:
 
            if e.key==K_q:
                link.rolling=True
            
           
            if e.key==K_SPACE:
                
                link.slashing=True
        
        if e.type==KEYUP:
        
            if page=="game":
                if link.rolling!=True:
                    if e.key==K_m:
                        minmaptoggle*=-1                   
                        blitback(backx,backy)
                    link.speed=link.inispeed
                    link.movement="walk"+link.direction
                    link.frame=0#animate adds one to frame so frame 0 will be shown
                    
    if page=="game":

 
        if link.rolling:
            link.roll()
        if link.slashing:
            link.slash()
        if link.state=="attack":
            link.checkcollide(enemysprites)
        
            
                    
        changeintime = clock.tick(60)/1000
     
        anicounter+=1
       

     
        
        for enemy in offscreenenemies:
            if enemy.location==(backx,backy):
                allsprites.add(enemy)
                offscreenenemies.remove(enemy)
                enemysprites.add(enemy)
            
        for enemy in enemysprites:
            if enemy.location!=(backx,backy):
                enemy.x,enemy.y=enemy.startpos[0],enemy.startpos[1]
                allsprites.remove(enemy)
                offscreenenemies.add(enemy)
                enemysprites.remove(enemy)
        for atk in enemyweaponsprites:
             if enemy.location!=(backx,backy):
                allsprites.remove(enemy)
                offscreenweapons.add(enemy)
                enemyweaponsprites.remove(enemy)

    #link walk and slash
        link.walk(keys)

        
        

    #enemy animation 
        if anicounter%2==0:
            for enemy in enemysprites:
                if enemy not in wizzrobesprites:

                    enemy.update()           
        else:
            for enemy in enemysprites:
                if enemy not in wizzrobesprites and enemy not in hadiesprites:
                
                    enemy.animate()
                    enemy.pathfind()
        if wizzrobesprites:
            for wizz in wizzrobesprites:
                if wizz in allsprites:
                    wizz.operate()
                else:
                    wizzflame.kill()
        else:
            wizzflame.kill()
        if hadiesprites:
            for hadiee in hadiesprites:
                if hadiee in allsprites:
                    hadiee.detect()
                    
                        
                else:
                    hadie.active=False
            

    #sentry
        for bullet in sentrybullets:
                bullet.work(changeintime)
        
                if link.state=="normal":
                    if bullet.checkcollide(mainsprite):
     #                   bullet.checkcollide(mainsprite)# if statement already does
            

                        bullet.reset()
                               
            
    #boomerang stuff
        boomer(angle,increment)
        if boomerang.shoot==True:
            angle+=10
            if angle<225:
                increment+=4
            else:
                increment-=4
            
            
            if angle==450:
                boomerang.shoot=False
                increment=1
                angle=0
    #check collide for boomerang arrow and item with link
        boomerang.checkcollide(enemysprites)
        if link.state=="normal":
            for i in enemysprites:
                i.checkcollide(mainsprite)
        arrowshoot()
        
        arrow.checkcollide(enemysprites)
        

        link.checkcollide(itemsprites)

        
        boomerang.checkcollide(itemsprites)
        
        if link.state=="hurt":
            hurttime+=1
        if hurttime:
            if hurttime<4:
                link.movement="hurt"+link.direction
            
                link.animate()
            if hurttime>15:
                link.state="normal"
                link.movement="walk"+link.direction
                link.frame=0
                link.animate()
                hurttime=0
        if link.state!="hurt":
            hurttime=0
        
    #draw
        drawall(backx,backy)
    if page=="settings":
        settingsmenu()
        display.update()
quit()
