from pygame import *
from math import *
from random import *
from glob import *
import pickle
from imageload import imageload
import os
from shopp import*

from Menu import menu
font.init()
init()
music=mixer.music.load("music/menumusic.mp3")

#mixer.music.play(-1)#music
page="game"#chooses page so settings or gme or shop
class game():
    def __init__(self,savefile):
        self.chan=mixer.Channel(4)
        self.chan.set_volume(0.3)
        self.sounds=[mixer.Sound(i) for i in glob("music/*.flac")]
        self.screen=display.set_mode(((800,740)),DOUBLEBUF|HWSURFACE)
        os.environ['SDL_VIDEO_CENTERED']='1'
        self.screenx=800
        self.screeny=740
        self.font=font.Font("ReturnofGanon.ttf",35)
        self.mx,self.my=mouse.get_pos()
        self.mb=mouse.get_pos()
        self.keys=key.get_pressed()
        self.changeintime=0
 
        self.curitemcounter=1#for bootom left corner box

         #sprites groups
        self.itemsprites=sprite.Group()
        self.allsprites=sprite.Group()
        self.enemysprites=sprite.Group()
        self.weaponsprites=sprite.Group()
        self.mainsprite=sprite.Group()
        self.offscreenenemies=sprite.Group()
        self.wizzrobesprites=sprite.Group()
        self.enemyweaponsprites=sprite.Group()
        self.offscreenweapons=sprite.Group()
        self.deadsprites=sprite.Group()
        self.sentrybullets=sprite.Group()
        self.hadiesprites=sprite.Group()
        self.bombarossasprites=sprite.Group()
        self.keysprites=sprite.Group()

        #items
        self.bkey=0


#background
        self.backx,self.backy=0,0#which part of the background is blit
        self.floors=imageload(glob("images/maps/*.png"),4,True)#all maps
        self.floors[2]=imageload("images/maps/houseinside.png",3.4)
        self.housemask=[loadMap(glob("housemask/("+str(i)+",*).txt")) for i in range(11)]
        self.insidehouse=[loadMap(glob("housemask/(-1,0).txt"))]

        
       
        
    
        self.visback=self.floors[1]#official variable for what is being blit
        self.floorbound=self.housemask[self.backx][self.backy]#official 2d mask

        self.minmaptoggle=-1#is map showing or not
        self.rupeenum=200#currency
 
        self.anicounter=0#slows animtion so things dont move too fast
    def controls(self):
        
        if self.keys[K_j]:
            boomerang.boomer()
        if self.keys[K_k]:
            bomb.bombthrow()
        if self.keys[K_l]:
            arrow.arrowshoot()
    def run(self):
        global page
        self.controls()
        for i in g.bombarossasprites:
            bomben.explode()
    
              
        
        self.changeintime = clock.tick(60)/1000
     
        self.anicounter+=1
       

     
        for enemy in self.offscreenenemies:#checks if enemies should be on screen and add them if they are supposed to be
            if enemy.location==(self.backx,self.backy):
                self.allsprites.add(enemy)
                self.offscreenenemies.remove(enemy)
                self.enemysprites.add(enemy)
                
        for enemy in self.enemysprites:#checks opposite of above comment
            if enemy.location!=(self.backx,self.backy):
                enemy.x,enemy.y=enemy.startpos[0],enemy.startpos[1]
                enemy.animate()
                self.allsprites.remove(enemy)
                self.offscreenenemies.add(enemy)
                self.enemysprites.remove(enemy)
                if enemy in self.hadiesprites:
                    enemy.movement="wakeup"
                enemy.frame=0
                enemy.animate()
        for atk in self.enemyweaponsprites:#these are enemyweapons like flame ball
             if enemy.location!=(self.backx,self.backy):
                self.allsprites.remove(enemy)
                self.offscreenweapons.add(enemy)
                self.enemyweaponsprites.remove(enemy)

    
        for ite in self.keysprites:
            if ite.location==(g.backx,g.backy):
                self.allsprites.add(ite)
                self.itemsprites.add(ite)
            else:
                self.allsprites.remove(ite)
        for enemy in self.enemysprites:#hurttime counter to slow down the killing of enemies
            if enemy.state=="hurt":
                enemy.hurttime+=1
                if enemy.hurttime>20:
                    enemy.hurttime=0
                    enemy.state="normal"
        if self.anicounter%2==0:
           
            for enemy in self.enemysprites:
                if enemy not in self.wizzrobesprites and enemy not in self.hadiesprites:#updates all "dumb" enemies that just pathfind
                    enemy.animate()
                    enemy.pathfind()
        if self.wizzrobesprites:#controls wizzrobesprites and if they are not on map remove them and their fireballs
            for wizz in self.wizzrobesprites:
                if wizz in self.allsprites:
                    wizz.operate()
                else:
                    wizz.atk.kill()
        else:
            wizzflame.kill()
        if link.rect.collidepoint(230,125) and (g.backx,g.backy)==(3,2):
            link.x,link.y=450,600
            link.animate()
            self.backx,self.backy=-1,0
        
            
            
            self.visback=self.floors[1]
            blitback()
        if link.rect.collidepoint(420,676) and (self.backx,self.backy)==(-1,0):
            
            self.backx,self.backy=3,2
            link.x,link.y=230,200
            link.animate()
            self.visback=self.floors[2]
            blitback()
        if link.rect.collidepoint(450,676) and (self.backx,self.backy)==(-1,0):
            self.backx,self.backy=3,2
            link.x,link.y=230,200
            link.animate()
            self.visback=self.floors[2]
            blitback()
        
        if link.rect.collidepoint(677,272) and (self.backx,self.backy)==(2,1):
            page="shop"
            
                    
                              
      
    
        if self.hadiesprites:#same for funny grass enemy
            for hadiee in self.hadiesprites:
                if hadiee in self.allsprites:
                    hadiee.detect()
                    
                        
                else:
                    hadie.active=False
                    hadie.frame=0
    
    #sentry
        for bullet in g.sentrybullets:#these are the sentry bullets that just chase you down if you are within range
                bullet.work()
        
                if link.state=="normal":
                    if bullet.checkcollide(g.mainsprite):
     #                   bullet.checkcollide(mainsprite)# if statement already does
            
         
                        bullet.reset()
        bomb.operate()#operating all weapons
        arrow.operate()
        boomerang.operate()
        if bomb.shoot and bomb.location!=(g.backx,g.backy):
 
            self.explode=False
            g.allsprites.remove(bomb)
            bomb.timer=False
            bomb.shoot=False
            bomb.frame=0
            bomb.varx=0
            bomb.location=(g.backx,g.backy)
            
   
            
                                                 
    

    #link collide checking and hurttime working
        link.perform()
        link.walk()

    
 
    




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
        "animates and updates character position"
        if self.frame>len(self.ani[self.movement]):
            self.frame=0
        if self.frame!=len(self.ani[self.movement]):#looping through animations

            self.image=(self.ani[self.movement][self.frame])#updating image and rect for sprite module
            self.rect=self.image.get_rect(center=(self.x,self.y))
            
            self.frame+=1
           
        else:
            self.frame=0
    def move(self):
        "moves character"
      
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
        if self in g.allsprites:
            
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
        g.sentrybullets.add(self)
  
    def distance(self):
        self.increment=link.x-self.x
        self.increment=link.y-self.y
    def approach(self):
        x_dist = link.x - self.rect.x
        y_dist = link.y - self.rect.y
        return atan2(-y_dist, x_dist) % (2 * pi)
    def work(self):
        self.reload += g.changeintime
        if self.range.contains(link.rect) and self.reload<2 and self.checkcollide(g.mainsprite)==False and self.location==(g.backx,g.backy): #homing bullets only last 2 seconds:
            
            g.allsprites.add(self)
 
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
        g.allsprites.remove(self)
    def checkcollide(self,group):
        if self in g.allsprites:
            
            if sprite.spritecollide(self,group,False):
                for i in (sprite.spritecollide(self,group,False)):
                    i.hurt()
                    return True
        
        return False
            
            
class item(sprite.Sprite):
    def __init__(self,image,effect,x=0,y=0,location=False):
        sprite.Sprite.__init__(self)
        self.x,self.y=x,y
        self.image=image[0]
        self.rect=Rect((self.x,self.y,self.image.get_width(),self.image.get_height()))
        self.effect=effect
        if not location:
            self.location=(g.backx,g.backy)
        else:
            self.location=location
    def appear(self,x,y):
        self.rect=Rect((x,y,self.image.get_width(),self.image.get_height()))
        g.allsprites.add(self)
    def hurt(self):
        g.itemsprites.remove(self)
        g.allsprites.remove(self)
        if self.effect=="rupeenum+=1":
            g.rupeenum+=1
       
        if self.effect=="link.health+=1":
            link.health+=1
        if self.effect=="bomb.ammo+=1":
            bomb.ammo+=1
        if self.effect=="arrow.ammo+=1":
            arrow.ammo+=1
        if self.effect=="rupeenum+=20":
            g.rupeenum+=20
        if self.effect=="bkey+=1":
            g.bkey+=1
            self.kill()
  
    
        
    
class zelda(gameobj):
    def __init__(self,sprites,speed,health,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        g.mainsprite.add(self)
        self.inispeed=self.speed
        self.health=health
        self.maxhealth=20
        self.state="normal"
        g.allsprites.add(self)
        self.slashing=False
        self.rolling=False
        self.hurttime=False
    def walk(self):
        
        if not bomb.animating :
  
            if g.keys[K_LEFT] or g.keys[K_a]:
                if g.anicounter%8==0:
                    g.chan.play(g.sounds[4])
                
                if link.rolling:
                    link.rolling=False
                link.direction="left"
                link.movement="walkleft"
                link.animate()
                
                link.move()
            
            if g.keys[K_RIGHT] or g.keys[K_d]:
                if g.anicounter%8==0:
                    g.chan.play(g.sounds[4])
                if link.rolling:
                    link.rolling=False
                link.direction="right"
                link.movement="walkright"
                link.animate()
                link.move()
                
            if g.keys[K_UP] or g.keys[K_w]:
                if g.anicounter%8==0:
                    g.chan.play(g.sounds[4])
                if link.rolling:
                    link.rolling=False
                link.direction="up"
                link.movement="walkup"
                link.animate()
                link.move()
                
            if g.keys[K_DOWN] or g.keys[K_s]:
                if g.anicounter%8==0:
                    g.chan.play(g.sounds[4])
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
            link.reset()
         
 
     
    def slash(self):
        self.movement="slash"+self.direction
        self.state="attack"
        self.animate()
        if len(self.ani[self.movement])==self.frame:
            self.slashing=False
            link.reset()
            self.state="normal"
            self.animate()
    
            
        
    def hurt(self):
        self.state="hurt"
 
        self.health-=1
        
        blitback()
        if self.health==0:
            self.movement="death"
            self.animate()
            time.wait(200)
    def perform(self):
        if self.state=="normal":
            for i in g.enemysprites:
                i.checkcollide(g.mainsprite)
            if bomb.explode:
                bomb.checkcollide(g.mainsprite)
        if self.checkcollide(g.itemsprites):
            blitback()
       
        
        if self.state=="hurt":
            self.hurttime+=1
        if self.hurttime:
            if self.hurttime<4:
                self.movement="hurt"+self.direction
            
                self.animate()
            if self.hurttime>15:
                self.reset()
                self.animate()
                self.hurttime=0
        if self.state!="hurt":
            self.hurttime=0
        if self.rolling:
            self.roll()
        if self.slashing:
            self.slash()
        if self.state=="attack":
            self.checkcollide(g.enemysprites)
 

    def bound(self):#makes sure that player stays in boundaries
 #       global backx,backy,visback,lostwoodsmask,floorbound
 
   
        if self.direction=="right":
            
            if (link.x+link.image.get_width())//20>39:
                
                g.backx+=1
                self.x-=780
                blitback()
            elif g.floorbound[(self.x)//20+1][self.y//20]==1:
                return False
            
              
        if self.direction=="left":
            if (self.x-5//20)<1 :
  
                g.backx-=1
                self.x+=780
                
                blitback()
            
            elif self.x//20-1!=-1:
                if g.floorbound[(self.x)//20-1][self.y//20]==1:
                  
                    return False
          
        if self.direction=="up":
            if link.y//20<1 :
                
                g.backy-=1
                self.y+=720
                blitback()
            elif g.floorbound[(self.x)//20][(self.y)//20-1]==1:
                return False
        if link.direction=="down":
            if (self.y+self.image.get_height())//20>37 :
                self.y-=720
                g.backy+=1
 
                self.animate()
                blitback()
            elif g.floorbound[(self.x)//20][self.y//20+1]==1:
 
                return False
     
        return True
    def reset(self):
        self.speed=self.inispeed
        self.movement="walk"+self.direction
        self.state="normal"
        self.frame=0#animate adds one to frame so frame 0 will be shown
        
class enemy(gameobj):
    def __init__(self,sprites,speed,health,location,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        self.startpos=(x,y)
        self.health=health
        g.enemysprites.add(self)
        self.location=location
        self.hurttime=0
        self.state="normal"
        g.offscreenenemies.add(self)

    def pathfind(self):#self is enemy
        ################################# nithin logic
        floor=g.floorbound
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
        if self.state!="hurt":
            self.health-=1
            if link.movement[0:5]=="slash":
                if link.direction=="left":
                    self.x-=50
                if link.direction=="right":
                    self.x+=50
                if link.direction=="up":
                    self.y-=50
                if link.direction=="down":
                    self.y+=50
      
        
            self.state="hurt"
            if self.health==0:
                self.kill()
                g.deadsprites.add(self)
                self.itemdrop()
  
        
    def itemdrop(self):
         itemdrop=choice(["rrupee"])
         dropchance=[1,1,1,1,1,1]
    
         if choice(dropchance)==1:
             if itemdrop=="grupee":
                 grupee=item(greenrupee,"rupeenum+=1")
                 g.itemsprites.add(grupee)
                 grupee.appear(self.x,self.y)
                 
             if itemdrop=="heart":
                 heartt=item(heartups,"link.health+=1")
                 g.itemsprites.add(heartt)
                 heartt.appear(self.x,self.y)
                 
                 
             if itemdrop=="arrow":
                 arrowup=item(arrow_up,"arrow.ammo+=1")
                 g.itemsprites.add(arrowup)
                 arrowup.appear(self.x,self.y)
             if itemdrop=="bomb":
                 bombup=item(bomb_up,"bomb.ammo+=1")
                 g.itemsprites.add(bombup)
                 bombup.appear(self.x,self.y)
             if itemdrop=="rrupee":
                 rrupee=item(redrupee,"rupeenum+=20")
                 g.itemsprites.add(rrupee)
                 rrupee.appear(self.x,self.y)
                
    def bound(self):#makes sure that player stays in boundaries
        return True
             
class wizzrob(enemy):
    def __init__(self,sprites,speed,health,x,y,location,atk,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        g.wizzrobesprites.add(self)
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
          
            while g.floorbound[teleport[0]][teleport[1]]==1 or sqrt((teleport[0]-self.x//20)**2+(teleport[1]-self.y//20)**2)<5:
                teleport=(randint(0,39),randint(0,36))
            self.x=teleport[0]*20
            self.y=teleport[1]*20

            
    def attack(self):
     
        if self.location==(g.backx,g.backy):
    
            if self.atk not in g.allsprites:
                g.allsprites.add(self.atk)
            if self.frame==len(self.ani[self.movement]) and self.attacking!=True:
                
                self.attacking=True
                g.allsprites.add(self.atk)
                self.atk.rect.x,self.atk.rect.y=self.x,self.y
            x_dist = link.x - self.atk.rect.x
            y_dist = link.y - self.atk.rect.y
            atkmove=atan2(y_dist, x_dist) % (2 * pi)
            self.atk.rect.x+=int(cos(atkmove) * self.speed)
            self.atk.rect.y+=int(sin(atkmove) * self.speed)
            if link.state=="normal":
                if self.atk.checkcollide(g.mainsprite):
                    self.attacking=False
        else:
            g.allsprites.remove(self.atk)
            self.attacking=False
            
                
    def operate(self):
            self.turn()
            self.disappear()
class hadi(enemy):
    def __init__(self,sprites,speed,health,location,x,y,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        g.hadiesprites.add(self)
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
class bombarossa(enemy):
    def __init__(self,sprites,speed,health,location,x,y,iniframe):
        
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        self.rng=10
        g.bombarossasprites.add(self)
        self.drop=False
        self.exploding=False
        self.bomb=bombweap(bombanimations,10,self.x,self.y,False,"bomb")
        
    def explode(self):
        if sqrt((self.x-link.x)**2+(self.y-link.y)**2)<100 or self.state=="hurt":
            if not self.drop:
                self.drop=True
                self.frame=0
        if self.drop:
            self.movement="explode"
            self.animate()

            if self.frame==len(self.ani[self.movement]):
     
                self.kill()
                g.deadsprites.add(self)
            
            
        
       
        
class weapon(gameobj):
    def __init__(self,sprites,speed,limit,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        self.equipped=False
        self.appear=False
        self.limit=limit
        self.shoot=False
        self.animating=True
        g.weaponsprites.add(self)
    def reset(self):
        self.remove(allsprites)
    def bound(self):
        return True
class throwingweap(weapon):
    def __init__(self,sprites,speed,limit,x,y,move):
        weapon.__init__(self,sprites,speed,limit,x,y,move)
        self.angle=20
        self.increment=1
        
    
    
    def boomer(self):
        if self.shoot!=True:
            g.allsprites.add(self)
            self.animating=True
            self.shoot=True
            self.x,self.y=link.x,link.y
    def operate(self):
        
        if self.shoot==True:
            self.animate()
            theta = radians(self.angle)
            self.x,self.y=link.x + self.increment * cos(theta), link.y+ self.increment* sin(theta)
        if self.shoot==False:
            g.allsprites.remove(self)
        if self.animating:
            link.movement="boomerang"+link.direction
            link.animate()
            if link.frame==len(self.ani[self.movement]):
                self.animating=False
        if self.shoot==True:
            self.angle+=10
            if self.angle<225:
                self.increment+=4
            else:
                self.increment-=4
            
            
            if self.angle==450:
                self.shoot=False
                self.increment=1
                self.angle=0
    #check collide for boomerang arrow and item with link
        self.checkcollide(g.enemysprites)
        if self.checkcollide(g.itemsprites):
            blitback()
class bombweap(weapon):
    def __init__(self,sprites,speed,limit,x,y,move):
        weapon.__init__(self,sprites,speed,limit,x,y,move)
        self.timer=1
        self.varx=1
        self.explode=False
        self.moving=False
        self.ammo=10
        self.location=(g.backx,g.backy)

    def bombthrow(self):
        if self.shoot==False:
            if g.keys[K_RIGHT] or g.keys[K_LEFT] or g.keys[K_a] or g.keys[K_d]:
                self.moving=True
            self.direction=link.direction
            if bomb.ammo!=0:
                self.frame=0
                self.animate()
                self.shoot=True
                g.allsprites.add(self)
            link.movement="throw"+link.direction
            g.location=(g.backx,g.backy)
            self.animating=True
            
 
 
            bomb.x,bomb.y=link.x,link.y-link.image.get_height()
            self.startx,self.starty=self.x,self.y
    def operate(self):
        if self.animating:
            link.movement="throw"+link.direction
            link.animate()
            if link.frame==len(link.ani[link.movement]):
                
                self.animating=False
        if bomb.shoot==True:
            
 
            if self.timer<40:
                
                
                if self.direction=="up" and bomb.starty-self.limit<self.y:
                    
                    bomb.y-=bomb.speed
 
            
                elif self.direction=="down" and bomb.startx+self.limit*2>self.y:
                    bomb.rect.y+=bomb.speed
            
           
                elif self.direction=="left":#and self.rect.x-self.speed>self.totalpos[0]-self.dist and self.rect.x-self.speed>0 and self.bombmove:
                    if self.moving:
                        self.x=self.startx-self.varx*15
                        self.y=self.varx**2-15*self.varx+self.starty
                    else:
                        self.x,self.y=self.startx-40,self.starty+40
                    
                elif self.direction=="right":#and self.rect.x+self.speed<self.totalpos[0]+self.dist and self.rect.x+self.speed<800 and self.bombmove:
                    if self.moving:
                        self.x=self.startx+self.varx*15
                        self.y=self.varx**2-15*self.varx+self.starty
                    else:
                        self.x,self.y=self.startx+20,self.starty+35
                bomb.rect.y=bomb.y
                bomb.rect.x=bomb.x
            else:
                self.explode=True
            if self.explode:
                self.moving=False
                self.checkcollide(g.enemysprites)
      
                
                self.animate()
               
                if self.frame==len(self.ani[self.movement]):
                    self.explode=False
                    g.allsprites.remove(self)
                    self.timer=False
                    self.shoot=False
                    self.frame=0
                    self.varx=0
                    self.ammo-=1
       
    
            if self.varx<17:
                self.varx+=1
            self.timer+=1
                    
                
      
class shootingweap(weapon):
    def __init__(self,sprites,speed,limit,x,y,move):
        weapon.__init__(self,sprites,speed,limit,x,y,move)
        self.arrowcounter=0
        self.ammo=5#ammo
    def arrowshoot(self):
   
        if self.shoot!=True:
            link.movement="bow"+link.direction
            self.arrowcounter+=1
            link.animate()
            if self.arrowcounter==len(link.ani[link.movement]) and self.ammo:
                self.ammo-=1
                self.direction=link.direction
                self.movement="arrow"+link.direction
                self.shoot=True
                self.x,self.y=link.x,link.y
                self.startx,self.starty=self.x,self.y
                self.animate()
                g.allsprites.add(self)
                self.arrowcounter=0
    def operate(self):
        if self.shoot==True:
            self.move()
            self.animate()
            if self.direction=="left":
                if self.startx-self.limit>self.x:
                    g.allsprites.remove(self)
                    self.shoot=False

            if self.direction=="right":
                if self.startx+self.limit<self.x:
                    g.allsprites.remove(self)
                    self.shoot=False

            if self.direction=="up":
                if self.starty-self.limit>self.y:
                    g.allsprites.remove(self)
                    self.shoot=False
                   
            if self.direction=="down":
                if self.starty+self.limit<self.y:
                    g.allsprites.remove(self)
      
                    self.shoot=False
            arrow.checkcollide(g.enemysprites)
        
def test():


    for x in range(len(g.floorbound)):
        for y in range(len(g.floorbound[x])):
            if g.floorbound[x][y]==1:
                draw.rect(g.screen,(255,255,255),(x*20,y*20,17,17))       
                

def blitback():
    if g.backx<0:
        g.visback=g.floors[2]
        g.screen.blit(g.visback,(0,0))
        
    if g.backx>4:
       
        if g.backx==5 and link.x<5:
            link.x+=20
    
        g.visback=g.floors[0]
        
        g.screen.blit(g.visback,(-800*(g.backx-5),-740*g.backy))
    elif g.backx<5:
        g.visback=g.floors[1]
        g.screen.blit(g.visback,(-800*g.backx,-740*g.backy))
    if g.backx<0:
        g.floorbound=g.insidehouse[g.backx][g.backy]
    else:
        g.floorbound=g.housemask[g.backx][g.backy]
    
        
    
def loadMap(fname):#sirs 2d list modded
    lis=[]
    for i in fname:
        
        myPFile = open(i, "rb")        # load my board that I pickled
        lis.append(pickle.load(myPFile))
    return lis
    

def drawall():                     
    if g.backx<0:
        
        g.visback=g.floors[2]
        g.allsprites.clear(g.screen,g.visback.subsurface(0,0,800,740))#did someth
        
    if g.backx>4:
        g.visback=g.floors[0]
        g.allsprites.clear(g.screen,g.visback.subsurface(800*(g.backx-5),740*g.backy,800,740))#did something weird when the background was not blit

        
    elif g.backx<5 and g.backx>-1:
        g.visback=g.floors[1]
    
        g.allsprites.clear(g.screen,g.visback.subsurface(800*g.backx,740*g.backy,800,740))#did something weird when the background was not blit
    if g.minmaptoggle==1:
        drawminmap()
    settings()
    updatehearts()
    s.rupeehandling(g.rupeenum)  
  
    showammo()

    g.allsprites.update()
    g.allsprites.draw(g.screen)
    display.flip()    
g=game(False)
s=shopclass(g.screen)


        
        
            
        
    
       

redrupee=[imageload(("images/items/redRupee.png"),0.02)]
greenrupee=[imageload(("images/items/GreenRupee.png"),0.02)]#glob all rupees
heartups=[imageload(("images/items/heart.png"),0.04)]
bomb_up=[imageload(("images/items/bomb.png"),0.2)]
arrow_up=[imageload(("images/items/arrow.jpg"),0.5)]
bosskey=[imageload(("images/items/keys.png"),0.1)]
b_key1=item(bosskey,"bkey+=1",250,250,(-1,0))
b_key2=item(bosskey,"bkey+=1",518,502,(5,1))
b_key3=item(bosskey,"bkey+=1",369,239,(7,4))
b_key4=item(bosskey,"bkey+=1",454,119,(0,2))
b_key5=item(bosskey,"bkey+=1",310,688,(1,0))
b_key6=item(bosskey,"bkey+=1",624,200,(1,2))
b_key7=item(bosskey,"bkey+=1",505,695,(4,2))
g.keysprites.add(b_key1,b_key2,b_key3,b_key4,b_key5,b_key7)

#ui
hylian = font.Font('ReturnofGanon.ttf', 35)

rupeescolon = hylian.render(':',False,(205,0,0))



ui = g.screen.subsurface(Rect(0,0,g.screenx,g.screeny))

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
ExitRect.center = g.screenx//2,395##g.g.screeny//2
ResumeRect = Resume.get_rect()
ResumeRect.center = g.screenx//2,325
SettingsMenuRect = Rect(0,0,150,298-10-ExitRect.bottomright[1]+ExitRect[1]-55-45+10)
SettingsMenuRect.midtop = g.screenx//2,298-10
gear_rect = Rect(gear.get_rect(x=755,y=10))


def drawminmap():
    minmap=transform.scale(g.visback,(200,200))
    minmaprect = g.visback.get_rect()
    
    draw.rect(ui,(255,215,0),(g.screenx-205,g.screeny-205,minmaprect[2]+5,minmaprect[3]))
 
    ui.blit(minmap,(g.screenx-200,g.screeny-200))
    if g.backx>4:
        linkmappos=(((g.backx-4)*800+link.x)//20,(g.backy*740+link.y)//20)
    else:
        linkmappos=((g.backx*800+link.x)//20,(g.backy*740+link.y)//20)
    
    
    draw.circle(g.screen,(255,0,0),(linkmappos[0]+577,linkmappos[1]+545),3)
def updatehearts(heartstatus=3,distapart=20):
    x,y = 3,0
    if heartstatus>0:
        for pos in range(link.health):
            ui.blit(heart,(x+distapart*pos,y))
def settings():
    global page
    ui.blit(gear,(755,10))
    
    
    if gear_rect.collidepoint(g.mx,g.my):
        ui.blit(gearhover,(755,10))
        if g.mb[0]==1:
            page="settings"
        
def settingsmenu(menuwallpadding=5):
    global page
    change=False
    draw.rect(ui,(255,215,0),SettingsMenuRect)#(ResumeRect[0]-menuwallpadding,ResumeRect[1]-menuwallpadding,ExitRect.bottomright[0]-ResumeRect.topleft[0]+15+menuwallpadding,ExitRect.bottomright[1]-ResumeRect.topleft[1]+15+menuwallpadding))
    ui.blit(Resume,ResumeRect)
    if ResumeRect.collidepoint(g.mx,g.my):
        ui.blit(ResumeHover,ResumeRect)
        if g.mb[0]==1:
            page="game"
            change=True
 
    ui.blit(Exit,ExitRect)
    if ExitRect.collidepoint(g.mx,g.my):
        ui.blit(ExitHover,ExitRect)
        if g.mb[0]==1:
            page="menu"
            change=True
    if change:
        blitback()
 
def showammo():
    draw.rect(ui,(255,215,0),(0,g.screeny-100,55,80))
    draw.rect(ui,(100,100,100),(0,g.screeny-95,50,70))
    ui.blit(bomb_ic,(5,g.screeny-90))
    ui.blit(arrow_ic,(5,g.screeny-50))
    
    bombstock = shop.hylian.render('%i'% bomb.ammo,False,(173,214,198))
    ui.blit(bombstock,(40,g.screeny-90))
        

    arrowstock = shop.hylian.render('%i'% arrow.ammo,False,(173,214,198))
    ui.blit(arrowstock,(40,g.screeny-50))

    
bomb_ic = imageload("images/UI/bomb.png",0.1,False,(255,255,255))
arrow_ic = imageload("images/UI/Arrow.png",0.175,False,(255,255,255))






###################################

    

####################################################################################################################################################       


#all backgrounds #all 2dlist floors are 40*40
#background main var is visback
dirnames=["left","right","up","down"]
linkanimations={k.split("/")[3]:imageload(glob(k+"/*.png"),2,True) for i in glob("images/link/*") for k in glob(i+"/*") }
sluganimations={k.split("/")[2]:imageload(glob(k+"/*.png"),2,True) for k in glob("images/slug/*") }
squidanimations={j:imageload(glob(k+"/*.png"),2,True) for k in glob("images/squid") for j in dirnames}
chuchuanimations={j:imageload(glob(k+"/*.png"),1,True) for k in glob("images/chuchu") for j in dirnames}
bombarossaanimations={k.split("/")[2]:imageload(glob(k+"/*"),2,True) for k in glob("images/bombenemy/*")}
wizzrobeanimations={k.split("/")[2]:imageload(glob(k+"/*.png"),2,True) for k in glob("images/wizzrobe/*") }
wizzrobeweaponanimations={"fire":[imageload("images/weapons/wizzrobeweapon/wizzrobeweapon0.png",2)]}
boomeranganimations={"boomer":imageload(glob("images/weapons/boomerang/*.png"),2,True,(0,0,0))}
bombanimations={"bomb":imageload(glob("images/weapons/bomb/*.gif"),2,True)}
bombanimations["bomb"].insert(0,imageload("images/weapons/bomb/0.png",0.45))

arrowanimations={"arrowup":[imageload("images/weapons/arrow/arrowup.png",0.5,(41,253,47))],
                 "arrowdown":[imageload("images/weapons/arrow/arrowdown.png",0.5,(41,253,47))],
                 "arrowleft":[imageload("images/weapons/arrow/arrowleft.png",0.5,(41,253,47))],
                 "arrowright":[imageload("images/weapons/arrow/arrowright.png",0.5,(41,253,47))]}
hadieanimations={k.split("/")[2]:imageload(glob(k+"/*.png"),3.7,True) for k in glob("images/hadienemy/*") }


#creating class objects
bomben=bombarossa(bombarossaanimations,5,2,(0,0),200,200,"down")
link=zelda(linkanimations,5,10,360,330,"walkleft")
hadie=hadi(hadieanimations,1,5,(4,0),200,300,"wakeup")
boomerang=throwingweap(boomeranganimations,10,200,link.x,link.y,"boomer")
arrow=shootingweap(arrowanimations,10,200,link.x,link.y,"arrowup")
bomb=bombweap(bombanimations,10,200,link.x,link.y,"bomb")

wizzflame=weapon(wizzrobeweaponanimations,6,100,0,0,"fire")
g.enemyweaponsprites.add(wizzflame)
   
#enemies #going to create enemy spawner from file io later and implement like item creation
#need to replace with for loop
wizzrobe=wizzrob(wizzrobeanimations,5,10,160,400,(2,0),wizzflame,"left")


#self,startx,starty,rng,location,speed=4,homing=False



for i in range(50,750,100):
    regbullet = sentrybullet(i,50,300,(2,0),7)
    homingbullet = sentrybullet(i,50,300,(2,0),7,True)
    
    




#clock object
clock=time.Clock()

#animation counter for enemies

def loadenemies(speed,health,ani=False,clas=enemy,file=""):
    epos=open("enemypos/Enemypos.txt").read().strip().split("\n")
    epos=[(i.split(" ")) for i in epos]
    
    for i in epos: 
        
        ani=choice((chuchuanimations,sluganimations,squidanimations))
        enem=clas(ani,5,2,(int(i[2]),int(i[3])),int(i[0]),int(i[1]),"left")
 #       self,sprites,speed,health,location,x,y,move
#loadenemies(5,2)


#event.set_grab(True)
shop=shopclass(g.screen)
blitback()
#blit the background
key.set_repeat(1,600)
running=True
page="game"
while running:
 

 
    g.keys=key.get_pressed()
    g.mx,g.my=mouse.get_pos()
    g.mb=mouse.get_pressed()
    clock.tick(60)
    if g.anicounter%50==0:
        print(clock.get_fps())
        print(g.mx,g.my)

    for e in event.get():
        
        if e.type == QUIT:
            running = False
        if e.type==KEYDOWN:
     
            if e.key==K_q:
                link.rolling=True
            
           
            if e.key==K_SPACE:
                
                link.slashing=True
        
        if e.type==KEYUP:
        
            
            if link.rolling!=True:
                
                link.reset()
            if e.key==K_m:
               
                g.minmaptoggle*=-1
                blitback()
                
    if page=="shop":
        shop.rupeenum=g.rupeenum
        add=shop.loop()
        bomb.ammo+=add[1]
        arrow.ammo+=add[2]
        link.health+=add[0]
 #       link.fairies+=add[3]
 #       g.hasmap=add[4]
 #       g.bosskeys+=add[5]
        g.rupeenum=add[6]
        page="game"
        blitback()
        link.x-=50
        link.frame=0
        link.animate()
         
    if page=="game":
        g.run()
       
        drawall()
    
    if page=="settings":    
        settingsmenu()
        display.update()
    if page=="menu":
        page=menu()
        
        blitback()
    
 #   if g.anicounter==200:
 #       print(True)
 #      for i in g.deadsprites:
 #           g.allsprites.add(i)
 #       
        
 #       page="game"
 
   # print(link.frame)
    #print(link.x,link.y)
       
    
quit()
