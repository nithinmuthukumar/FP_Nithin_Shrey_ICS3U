#Nithin Muthukumar Shrey Mahey
#Friday june 15th
#this is a legend of zelda topdown game where the objective is to collect keys scattered across the map and then enter the coliseum and defeat the boss
#You play as link and you have three weapon which are the arrow , the boomerang and the bomb
#many different types of enemies that pathfind and the special ones include wizzrobe which soots fireballs,
#bombenemy which explodes when it gets near you and explodes.
#hadie enemy which is a grass mob that camouflages
#there is a shop run by an old lady that sells ammo, health, a key, 3 fairies and a map which is almost essential for winning
#because it allows you to find the keys spots
#there are two main maps with lost woods which can be entered from the boundary on the right side.
#you can also save game from the settings which is opened by pressing the gear in the top right corner


from ScrollTextClass_and_OpeningCredits import*
from pygame import *
from math import *
from random import *
from glob import *
import pickle
from imageload import imageload
import os
from shop import*
from queue import*
from Menu import menu

font.init()
init()
sep=os.sep
def lood():
        if os.path.isfile("savedat"):
            if os.stat("savedat").st_size!=0:
                savedat = pickle.load(open("savedat","rb"))#load dictionary from pickle file
                return savedat
        
        
def save():
        savedat = {"hearts":link.health,"bkeys":g.bkey,"posx":link.x,"posy":link.y,"location":(g.backx,g.backy),"rupee":g.rupeenum,"arrow":arrow.ammo,"bomb":bomb.ammo,"hasmap":g.hasmap,"fairy":link.fairy,"keysleft":[[i.x,i.y,i.location] for i in g.keysprites]}
 #                  ,bkeys_bought:True,fairies_bought:0,hearts_bought:0}
       
        open("savedat","wb").close()
        pickle.dump(savedat,open("savedat","wb"))
                
        
    

music=mixer.music.load("music/menumusic.mp3")

mixer.music.play(-1)#music
mixer.music.set_volume(0.3)
page="game"#chooses page so settings or gme or shop
class game():
        #included all these extra things in initialization that I could have just done outside 
    def __init__(self):
        
        self.lood=lood()#loaded file from savedat
        self.chan=mixer.Channel(4)#to play music at diff volume from sound
        self.chan.set_volume(1)
        self.sounds=[mixer.Sound(i) for i in glob("music/*.flac")]
        self.screen=display.set_mode(((800,740)),DOUBLEBUF|HWSURFACE)
        os.environ['SDL_VIDEO_CENTERED']='1'#center screen
        self.screenx=800
        self.screeny=740
        self.font=font.Font("ReturnofGanon.ttf",35)
        self.mx,self.my=mouse.get_pos()
        self.mb=mouse.get_pos()
        self.keys=key.get_pressed()
        self.changeintime=0
        self.hasmap=self.lood["hasmap"]#if player has self
       

         #sprites groups for checking collision, drawing and interacting
        self.itemsprites=sprite.Group()#for items
        self.allsprites=sprite.Group()#everything that is drawn is in here
        self.enemysprites=sprite.Group()#all enemy
        self.weaponsprites=sprite.Group()
        self.mainsprite=sprite.Group()#link
        self.offscreenenemies=sprite.Group()
        self.wizzrobesprites=sprite.Group()
        self.enemyweaponsprites=sprite.Group()
        self.offscreenweapons=sprite.Group()
        self.deadsprites=sprite.Group()
        self.sentrybullets=sprite.Group()
        self.hadiesprites=sprite.Group()
        self.bombarossasprites=sprite.Group()
        self.keysprites=sprite.Group()
        self.bossprites=sprite.Group()

        #items
        self.bkey=self.lood["bkeys"] #key numbers
        
        
 

#background
        self.backx,self.backy=self.lood["location"]#which part of the background is blit slices 2d list of 2dlist masks to determine which on is used

        self.floors=imageload(glob("images/maps/*.png"),4,True)#all maps
        self.floors[2]=imageload("images/maps/2.png",3.4)
        self.housemask=[loadMap(glob("housemask/("+str(i)+",*).txt")) for i in range(11)]#2d lists for collision
        self.insidehouse=[loadMap(glob("housemask/(-1,0).txt"))]#these two are the only negative ones because they are not part of the main maps
        self.coliseum=[loadMap(glob("housemask/(-2,0).txt"))]
        self.floors[3]=imageload("images/maps/3.png",1)
    
        
       

 
       
        
    
        self.visback=self.floors[1]#official variable for what is being blit
        self.floorbound=self.housemask[self.backx][self.backy]#official 2d mask

        self.minmaptoggle=-1#is map showing or not
        self.rupeenum=self.lood["rupee"]#amount of currency to buy stuff
 
        self.anicounter=0#slows animtion so things dont move too fast
    def controls(self):
        
        if self.keys[K_j]:#weapons
            boomerang.boomer()
        if self.keys[K_k]:
            bomb.bombthrow()
        if self.keys[K_l]:
            arrow.arrowshoot()
    def run(self):
    
        global page#controls if you are on shop or exiting
        self.controls()#for weapon shots
        for i in g.bombarossasprites:
            i.explode()#check if explosion
    
        if self.bkey>8:
            for i in g.sentrybullets:
                i.kill()#get rid of sentries so that you can enter coliseum
        link.health+=1
       
        self.changeintime = clock.tick(60)/1000
     
        self.anicounter+=1# general counter to make some things slower
    
    
        
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
                if enemy in self.hadiesprites:# reset enemy
                    enemy.movement="wakeup"
                enemy.frame=0
                enemy.animate()
        for atk in self.enemyweaponsprites:#these are enemyweapons like flame ball
             if enemy.location!=(self.backx,self.backy):
                self.allsprites.remove(enemy)
                self.offscreenweapons.add(enemy)
                self.enemyweaponsprites.remove(enemy)
        for ite in self.keysprites:# make key appear
            if ite.location==(g.backx,g.backy):
                self.allsprites.add(ite)
                self.itemsprites.add(ite)
            else:
                self.allsprites.remove(ite)
    
        for ite in self.itemsprites:# if link goes to next location disappear or appear
            if ite.location==(g.backx,g.backy):
                self.allsprites.add(ite)
                self.itemsprites.add(ite)
            else:
                self.allsprites.remove(ite)
                if ite not in self.keysprites:
                    self.itemsprites.remove(ite)
        for enemy in self.enemysprites:#hurttime counter to slow down the killing of enemies
            if enemy.state=="hurt":
                enemy.hurttime+=1
                if enemy.hurttime>20:
                    enemy.hurttime=0
                    enemy.state="normal"
                
        if self.anicounter%2==0:
           
            for enemy in self.enemysprites:
                if enemy not in self.wizzrobesprites and enemy not in self.hadiesprites and enemy not in self.bossprites: #updates all "dumb" enemies that just pathfind
                    enemy.animate()
                    enemy.pathfind()
       
        if link.rect.colliderect((184,94,64,30)) and (g.backx,g.backy)==(3,2):# go from map to house
                
            link.x,link.y=450,600
            link.animate()
            self.backx,self.backy=-1,0
            
        
            
            
            self.visback=self.floors[1]
            blitback()
        if link.rect.colliderect((230,676,220,30)) and (self.backx,self.backy)==(-1,0):#go from house to map
            
            self.backx,self.backy=3,2
            link.x,link.y=230,200
            link.animate()
            self.visback=self.floors[2]
            blitback()
        
        if link.rect.colliderect((252,60,318,70)) and (self.backx,self.backy)==(2,0):#if link is in the place to go to next map
            self.backx,self.backy=-2,0#link moves to coliseum
            link.x,link.y=400,700
            link.animate()
            self.visback=self.floors[3]
            blitback()
        
        if link.rect.collidepoint(677,290) and (self.backx,self.backy)==(2,1):
            page="shop"#if link is at shop switch to shop
        if Rect((389,392,109,106)).collidepoint(g.mx,g.my) and (self.backx,self.backy)==(3,1):
                if e.type==MOUSEBUTTONDOWN:#for music switch
                        mixer.music.stop()
                        file=choice(glob("music/Songs/*.mp3"))
                        print(file)
                        
                        
                        music=mixer.music.load(file)
                
                        mixer.music.play(1)
                            
                              
      
    
        if self.hadiesprites:#same for funny grass enemy
            for hadiee in self.hadiesprites:
                if hadiee in self.allsprites:
                    hadiee.detect()#if link is close enough attack 
                    
                        
                else:
                    hadiee.active=False# if hadie is offscreen reset him- debugging
                    hadiee.frame=0
    
    #sentry
        for bullet in g.sentrybullets:#these are the sentry bullets that just chase you down if you are within range
                bullet.work()
        
                if link.state=="normal":#check il link is hit by sentrybullets
                    if bullet.checkcollide(g.mainsprite):
     #                   bullet.checkcollide(mainsprite)# if statement already does
            
         
                        bullet.reset()
        bomb.operate()#operating all weapons
        arrow.operate()
        boomerang.operate()
        if bomb.shoot and bomb.location!=(g.backx,g.backy):#to make bomb disappear when you move maps - debugging
 
            self.explode=False
            g.allsprites.remove(bomb)
            bomb.timer=False
            bomb.shoot=False
            bomb.frame=0
            bomb.varx=0
            bomb.location=(g.backx,g.backy)
            
        if self.wizzrobesprites:#controls wizzrobesprites and if they are not on map remove them and their fireballs
            for wizz in self.wizzrobesprites:
                if wizz in self.allsprites:
      
 #                       g.allsprites.add(wizz.atk)
                        wizz.operate()
 #               else:
                       
 #                       if wizz.location==(g.backx,g.backy):
 #                              g.allsprites.remove(wizz.atk)
        if wizzflame in g.allsprites:
                if (g.backx,g.backy)!=(2,0) and (g.backx,g.backy)!=(4,0) and (g.backx,g.backy)!=(4,2):
                        g.allsprites.remove(wizzflame)
       
               
                
                
   
            
   
            
                                                 
    

    #link collide checking and hurttime working
        link.perform()
        link.walk()

        if (g.backx,g.backy)==(-2,0):#do the minotaur movements if in coliseum
            g.allsprites.add(minotaur)
            minotaur.phases()
        
            
 
    




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
    def animate(self):#loops through frames and sets 
        "animates and updates character position"
        if self.frame>len(self.ani[self.movement]):#resets frame
            self.frame=0
        if self.frame!=len(self.ani[self.movement]):#looping through animations

            self.image=(self.ani[self.movement][self.frame])#updating image and rect for sprite module
            self.rect=self.image.get_rect(center=(self.x,self.y))
            
            self.frame+=1
           
        else:
            self.frame=0
    def move(self):
        "moves character"
     
        if self.direction=="left" and self.bound(): #makes sure player is not off map or bumping for link
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
    def checkcollide(self,group):#checks collision and hurts the object in the group
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
        return atan2(-y_dist, x_dist) % (2 * pi)#trig to find the pos
    def work(self):#moves towards the player
        self.reload += g.changeintime
        if self.range.contains(link.rect) and self.reload<2 and self.checkcollide(g.mainsprite)==False and self.location==(g.backx,g.backy): #homing bullets and its in range only last 2 seconds:
            
            g.allsprites.add(self)
 
            if self.homing:
                self.pos2 = self.approach()
               
            elif not self.homing and not self.pos2:
                distformula = sqrt((link.x - self.rect.x)**2 + (link.y - self.rect.y)**2)
                if distformula!=0:
                    self.rect.x+= ((link.x - self.rect.x) / distformula)*self.speed#moves towards link
                    self.rect.y+= ((link.y - self.rect.y) / distformula)*self.speed

            if self.pos2 and self.range.contains(self.rect) and self.homing:
              #if approach doesnt return False -- no 0
                self.rect.x += (cos(self.pos2) * self.speed)     #change in x
                self.rect.y -= (sin(self.pos2) * self.speed)     #change in y
        
            
         
        else:
            self.reset()
 
    def reset(self):
        
        self.reload=0
        self.rect.x=self.spawnspot[0]#resets enemies to their previous positions when they are offscreen
        self.rect.y=self.spawnspot[1]
        g.allsprites.remove(self)
    def checkcollide(self,group):
        if self in g.allsprites:# to make sure you are not colliding with something offscreen
            
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
    def appear(self,x,y):#makes the item appear
        self.rect=Rect((x,y,self.image.get_width(),self.image.get_height()))
        g.allsprites.add(self)
    def hurt(self):
        if self in g.keysprites:# if its a key do this seperately because ther was a bug
            if self.location==(g.backx,g.backy):
                if self.effect=="bkey+=1":

                    g.bkey+=1
                    self.kill()
  
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
                
    
        
    
class zelda(gameobj):
    def __init__(self,sprites,speed,health,x,y,move):
        gameobj.__init__(self,sprites,x,y,speed,move)
        g.mainsprite.add(self)
        self.inispeed=self.speed
        self.fairy=0
        self.health=health
        self.maxhealth=20
        self.state="normal"
        g.allsprites.add(self)
        self.slashing=False
        self.rolling=False
        self.hurttime=False
    def walk(self):
        
        if not bomb.animating:#so that the bomb throwing animates even if running

  
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
        
 
        self.movement="roll"+self.direction#roll and he goes faster
        self.speed+=1
        self.animate()
        self.move()
    
    
        if len(self.ani[self.movement])==self.frame:
            

            self.rolling=False
            link.reset()
         
 
     
    def slash(self):
        self.movement="slash"+self.direction
        self.state="attack"
        if g.anicounter%2==0:#to make slash last longer
            self.animate()
        if len(self.ani[self.movement])==self.frame:
            g.chan.play(g.sounds[4])
            self.slashing=False
            link.reset()
            self.state="normal"
            self.animate()
    
            
        
    def hurt(self):
        self.state="hurt"
 
        self.health-=1
        
        blitback()
        if self.health<=0:
            if not self.fairy:#if link has a fairy he gets 5 hearts
   
                self.movement="death"
                self.animate()
                drawall()
       
                time.wait(1000)
                
                import GameOver#if hes dead
            else:
                self.health+=5
                self.fairy-=1
                
    def perform(self):
 
        if self.state=="normal":#if link is not attacking check if enemy is hurting him
            for i in g.enemysprites:
                if i not in g.bossprites:
                        i.checkcollide(g.mainsprite)
            if bomb.explode:
                bomb.checkcollide(g.mainsprite)
        if self.checkcollide(g.itemsprites):#check if he touches the item
            blitback()
       
        
        if self.state=="hurt":#hurttimer so he doesnt lose hearts in a second
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
            
            if (link.x+link.image.get_width())//20>39:#if link is going off the map change map
                
                g.backx+=1
                self.x-=780
                blitback()
            elif g.floorbound[(self.x)//20+1][self.y//20]==1:#if link is bumping into wall (2dmask)
                g.chan.play(g.sounds[5])
                return False
            
              
        if self.direction=="left":
            if (self.x-5//20)<1 :
  
                g.backx-=1
                self.x+=780
                
                blitback()
            
            elif self.x//20-1!=-1:
                if g.floorbound[(self.x)//20-1][self.y//20]==1:
                    g.chan.play(g.sounds[5])
                    return False
          
        if self.direction=="up":
            if link.y//20<1 :
                
                g.backy-=1
                self.y+=720
                blitback()
            elif g.floorbound[(self.x)//20][(self.y)//20-1]==1:
                g.chan.play(g.sounds[5])
                return False
        if link.direction=="down":
            if (self.y+self.image.get_height())//20>37 :
                self.y-=720
                g.backy+=1
 
                self.animate()
                blitback()
            elif g.floorbound[(self.x)//20][self.y//20+1]==1:
                g.chan.play(g.sounds[5])
                return False
     
        return True
    def reset(self):
        self.speed=self.inispeed#to reset speed and other things after roll or slash
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


    def pathfind(self,x=0,y=0):#self is enemy
        ################################# not nithin logic anymore
        if not x:
            x=link.x
            y=link.y
        def dirs(i,d):
            return i[0]+d[0],i[1]+d[1]
        def heuristic(linkx,linky,x,y):
            
            dist=abs(linkx-x)+abs(linky-y)#gives manhattan distance
         
            
            return dist
                
        def astar(self):
            floor=g.floorbound#2d list mask
            directions=[(1, 0), (0, 1), (0, -1), (-1, 0)]#to make all four direction to move
            start=(self.x//20,self.y//20)
            end=(x//20,y//20)
   
     
            
            frontier=PriorityQueue()#creates a queue which has priorities and stores the one that is closest
            frontier.put((0,start))#adds start
            camefrom={}#stores parents
            cost_so_far={}#cost
            camefrom[start]=None
            cost_so_far[start]=0
            trace=end
            if start!=end:
                while not frontier.empty():#checks if queue is empty
                    current=frontier.get()#removes priority value
                    current = current[1]
                    if current==end:#the pathfinding is done if end is reached
                        
          
                        break
                    for d in directions:#loop through all four directions
                        nex_t=dirs(current,d)#gives the next value
                        if 0<=nex_t[0]<=39 and 0<=nex_t[1]<=36:#if the path is not out of bounds
                            if floor[nex_t[0]][nex_t[1]]==0 :#slice 2d list 
                                new_cost=cost_so_far[current]+1#the cost for nex_t g cost
                                if nex_t not in cost_so_far or new_cost<cost_so_far[nex_t]:#to make sure we are not on the same square again unless the cost is less
                                    cost_so_far[nex_t]=new_cost#assigns the cost to that square
                                    priority=new_cost+heuristic(nex_t[0],nex_t[1],end[0],end[1])#gives priority level for queue using manhattan distance and parent costs
                                    frontier.put((priority,nex_t))#puts nex_t in queue
                
                                    camefrom[nex_t]=current#assigns parent
                if not frontier.empty():
                   
                    while camefrom[trace]!=start:#loops through camefrom to find step from start
                        trace=camefrom[trace]
                    
                        
                    diffx=trace[0]-start[0]
                    diffy=trace[1]-start[1]
                    
               
                    if abs(diffx)>abs(diffy):
                        if diffx==-1:
                            self.movement="left"
                        elif diffx==1:
                            self.movement="right"
                    

         
                    else:
                        if diffy==-1:
                            self.movement="up"
                        elif diffy==1:
                            self.movement="down"
                    self.direction=self.movement
                        
                        
                    self.move()
 
                
            
                
        if 0<=link.x//20<=40 and 0<=link.y//20<=37:
            astar(self)#calls astar if link is not off map
 
            
                
                                                                          
    def hurt(self):
        
        if self.state!="hurt":
            self.health-=1
            if self not in g.bossprites:#knockback
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
                        g.deadsprites.add(self)#kills enemy
                        self.itemdrop()
        if self in g.bossprites:
                self.health-=1
          
        
    def itemdrop(self):#when enemy dies there is a chance fr it to drop an item
         itemdrop=choice(["rrupee","grupee","heart","arrow","bomb"])#chooses between items
         dropchance=[1,1,1,1,0,0]
    
         if choice(dropchance)==1:
             if itemdrop=="grupee":
                 grupee=item(greenrupee,"rupeenum+=1")#initializes item and calls appear mathod
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
class boss(enemy):
    def __init__(self,sprites,speed,health,x,y,location,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
  
        g.bossprites.add(self)
        
        self.startx,self.starty,self.speed,self.stren,self.rushtime,self.tired,self.slowed = self.x,self.y,2,2,0,False,False
        self.x,self.y = self.startx,self.starty
        self.hbar = imageload("HealthBar3.png",0.5,False,(255,255,255))
        self.hrect = self.hbar.get_rect()
        self.hrect.center = (g.screen.get_size()[0]//2,g.screen.get_size()[1]-35)
        self.attack=False
        self.attacking=False
        self.attackcounter=0
   
    def approach(self):
        x_dist = link.x - self.x
        y_dist = link.y - self.y
        return atan2(-y_dist, x_dist) % (2 * pi)
    def set_direction(self):#turns toward link
       
        olddir=self.direction
        diffx=self.x-link.x
        diffy=self.y-link.y
        if abs(diffx)>abs(diffy):
            if diffx>0:
                self.direction="left"
            if diffx<0:
                self.direction="right"
        else:
            if diffy<0:
                self.direction="down"
            if diffy>0:
                self.direction="up"
        if not self.slowed and not self.tired:
            self.movement="charge"+self.direction
            
            
            
     
        elif self.slowed and not self.tired:
            self.movement=self.direction
        elif self.tired:
          
            self.movement="hurt"
            
        self.animate()
    def drawhealthbar(self):#draws healthbar
        draw.rect(g.screen,(255,0,0),(self.hrect.x,self.hrect.y,self.hrect.width//45*self.health,self.hrect.height))
        g.screen.blit(self.hbar,self.hrect)
   
        
            
        

    def phases(self):
        if self.health<=0:
            import GameWin
        self.drawhealthbar()
        
    
        
            
       
        if self.health>25:
            self.phase1()
        if 30>self.health<25:
            self.phase2()
        
        if not self.tired:
            self.checkcollide(g.mainsprite)
        
            
##        print(self.allphases,len(self.allphases))
    def rush(self,timer):
        #print(self.speed)
        self.rushtime+=timer
##        if self.tired:
##            self.speed = 0
##            if self.rushtime>2500:
##                self.tired,self.rushtime = False,0
##        if self.slowed:
##            self.speed = 2
##            print(True)
##            if self.rushtime>2500:
##                self.tired,self.slowed = True,False
##        if self.rushtime>2000 and not self.slowed and not self.tired:
##            self.speed = 5
##            if self.rushtime>4000:
##                self.speed,self.rushtime = 2,0
##                self.slowed = True
        if self.tired:
            self.speed = 0
            if self.rushtime>2500:
                self.tired,self.slowed,self.rushtime = False,True,0
        if self.slowed:
            self.speed = 2
##            print(True) 
            if self.rushtime>2500:#add speed and attack
                self.tired,self.slowed = False,False
        if self.rushtime>2000 and not self.slowed and not self.tired:
            self.speed = 5
            if self.rushtime>4000:
                self.speed,self.rushtime = 2,0
                self.tired = True
    def phase1(self):#rushes at player
        self.rush(clock.get_time())
        self.pos2 = self.approach()
##        print(self.rect.x,self.rect.y)
        if not self.rect.collidepoint(link.rect.center) and not self.slowed:
            self.set_direction()
                
            self.x += round(cos(self.pos2) * self.speed)
            self.y -= round(sin(self.pos2) * self.speed)
        if self.slowed:
            
            self.pathfind()
            self.animate()
        
 
           
    def phase2(self):
        if not self.attacking and not self.tired:##it chases link then attacks
            self.pathfind()#chases player
            self.animate()
            self.speed=7
        if sqrt((self.x-link.x)**2+(self.y-link.y)**2)<80 and not self.attacking:
            self.attacking=True
            self.movement="attack"+self.direction
            self.animate()
        if self.attacking:
            self.attackcounter+=1
            if self.attackcounter==10:
                self.attack=True
        if self.attack:
            self.animate()
            
            if self.frame==len(self.ani[self.movement]):
                self.attackcounter=0
                self.attack=False
                self.attacking=False
                self.tired=True
        if self.tired:#tired timer
                self.rushtime+=1
                if self.rushtime>2500:
                        self.tired = False
                
                
            
            
            
        
            
            
            
            
            
            
    
    
    def updatehealth(self):#update healthbar
        draw.rect(screen,(255,0,0),(self.hrect.topleft[0]+40,self.hrect.topleft[1]+6,self.hrect.bottomright[0]-self.hrect.bottomleft[0]-self.hcounter,self.hrect.bottomright[1]-self.hrect.topright[1]-11))#self.hcounterrect)
        screen.blit(self.hbar,self.hrect)
        
             
class wizzrob(enemy):
    def __init__(self,sprites,speed,health,x,y,location,atk,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        g.wizzrobesprites.add(self)
        self.atk=atk
        self.attacking=False
        self.attackcount=0
        
    def turn(self):#turns towards player
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
        
            
    def disappear(self):#if player gets too close he teleports to somewhere else
        teleport=(self.x//20,self.y//20)
        if sqrt((self.x-link.x)**2+(self.y-link.y)**2)<100:#if their very close disappear
          
            while g.floorbound[teleport[0]][teleport[1]]==1 or sqrt((teleport[0]-self.x//20)**2+(teleport[1]-self.y//20)**2)<5:
                teleport=(randint(0,39),randint(0,36))
            self.x=teleport[0]*20
            self.y=teleport[1]*20

            
    def attack(self):
     
        if self.location==(g.backx,g.backy):#if he's on screen make the atk move towards the player
            
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
            self.attackcount+=1
            if link.state=="normal":
                if self.atk.checkcollide(g.mainsprite):# if it touches link it resets
                    self.attacking=False
                    self.attackcount=0
            if self.attackcount==60:#if the fire ball has lasted long enough reset
                self.attackcount=0
                self.attacking=False
                    
        else:
            self.attacking=False
            self.attackcount=0
            
                
    def operate(self):
            self.turn()
            self.disappear()
class hadi(enemy): # the grass enemy camouflage
    def __init__(self,sprites,speed,health,location,x,y,iniframe):
        enemy.__init__(self,sprites,speed,health,location,x,y,iniframe)
        g.hadiesprites.add(self)
        self.rng=10
        self.active=False
    def detect(self):#if hes close wakeup and attack
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
       
        
    def explode(self):
        if sqrt((self.x-link.x)**2+(self.y-link.y)**2)<100 or self.state=="hurt":#if he's close enough or he explodes
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
        self.animating=False
        g.weaponsprites.add(self)
 
    def bound(self):# so that the move function in gamobj does not care about boundaries
        return True
class throwingweap(weapon):
    def __init__(self,sprites,speed,limit,x,y,move):
        weapon.__init__(self,sprites,speed,limit,x,y,move)
        self.angle=20
        self.increment=1
        
    
    
    def boomer(self):
        if self.shoot!=True:# adds boomerang and starts the movement
            g.allsprites.add(self)
            self.animating=True
            self.shoot=True
            self.x,self.y=link.x,link.y#start position
    def operate(self):
        
        if self.shoot==True:
            self.animate()
            theta = radians(self.angle)#angle in radians at which boomerang approachs link
            self.x,self.y=link.x + self.increment * cos(theta), link.y+ self.increment* sin(theta)#calculates the next position for the boomerang, and sets the boomerangs position to it
        if self.shoot==False:
            g.allsprites.remove(self)
        if self.animating:#if the charaxcter is still not done the throwing motion
            link.movement="boomerang"+link.direction
            link.animate()
            if link.frame==len(self.ani[self.movement]):
                self.animating=False
        if self.shoot==True:
            self.angle+=10
            if self.angle<225:
                self.increment+=4#this makes the boomerang go away then come back
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
        self.timer=1#to make explode after a certain amount of time
        self.varx=1# the parabola x val
        self.explode=False
        self.moving=False
        self.ammo=g.lood["bomb"]
        self.location=(g.backx,g.backy)

    def bombthrow(self):
        if self.shoot==False:
            if g.keys[K_RIGHT] or g.keys[K_LEFT] or g.keys[K_a] or g.keys[K_d] or g.keys[K_DOWN] or g.keys[K_UP] or g.keys[K_w] or g.keys[K_s]:
                self.moving=True#if you are moving it throws the bomb instead of placing it
            self.direction=link.direction
            if bomb.ammo!=0:# to make sure you cant use bomb when ammo is gone
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
            if link.frame==len(link.ani[link.movement]):#make sure it animates before throw
                
                self.animating=False
        if self.shoot==True:
            
 
            if self.timer<40:
                
                
                if self.direction=="up":
                    if self.moving:
                        if bomb.starty-self.limit<self.y:
                            bomb.y-=bomb.speed
                        
                    else:
                        self.x,self.y=self.startx,self.starty-10
 
            
                elif self.direction=="down":
                    if self.moving:
                        if bomb.starty+self.limit>self.y:
                            bomb.y+=bomb.speed
                        
                    elif not self.moving:
                        self.x,self.y=self.startx,self.starty+40
                    
                    
            
           
                elif self.direction=="left":#and self.rect.x-self.speed>self.totalpos[0]-self.dist and self.rect.x-self.speed>0 and self.bombmove:
                    if self.moving:
                        self.x=self.startx-self.varx*15
                        self.y=self.varx**2-15*self.varx+self.starty
                    else:
                        self.x,self.y=self.startx-40,self.starty+40
                    
                elif self.direction=="right":#and self.rect.x+self.speed<self.totalpos[0]+self.dist and self.rect.x+self.speed<800 and self.bombmove:
                    if self.moving:
                        self.x=self.startx+self.varx*15#parabolas
                        self.y=self.varx**2-15*self.varx+self.starty
                    else:
                        self.x,self.y=self.startx+20,self.starty+35
                self.rect.y=bomb.y#to make sure the bomb x is reflected on the screen
                self.rect.x=bomb.x
            else:
                self.explode=True#if its over the timer it explodes
            if self.explode:
                self.moving=False
                self.checkcollide(g.enemysprites)
      
                
                self.animate()
               
                if self.frame==len(self.ani[self.movement]):#resets the bomb after explosion
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
        self.arrowcounter=0# for timer
        self.ammo=g.lood["arrow"]#ammo
    def arrowshoot(self):
   
        if self.shoot!=True:#this is to make sure it goes through the animations before the arrow is shot
            link.movement="bow"+link.direction
 
            self.arrowcounter+=1
            link.animate()
            if self.arrowcounter==len(link.ani[link.movement]) and self.ammo:# if the animation is over set everything and go
 
                self.ammo-=1
                self.direction=link.direction
                self.movement="arrow"+link.direction
                self.shoot=True
                self.x,self.y=link.x,link.y
                self.startx,self.starty=self.x,self.y
                self.animate()
                g.allsprites.add(self)
                self.arrowcounter=0
                g.chan.play(g.sounds[0])
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
    return

    for x in range(len(g.floorbound)):
        for y in range(len(g.floorbound[x])):
            if g.floorbound[x][y]==1:
                draw.rect(g.screen,(255,255,255),(x*20,y*20,17,17))       
                

def blitback():#It only blitbacks very time I need to so that especially on mac I can keep the framerate high
    if g.backx==-1:
        g.visback=g.floors[2]
        g.screen.blit(g.visback,(0,0))
    if g.backx==-2:
       
        g.visback=g.floors[3]
        g.screen.blit(g.visback,(0,0))
        
    if g.backx>4:
       
        if g.backx==5 and link.x<5:
            link.x+=20
    
        g.visback=g.floors[0]
        
        g.screen.blit(g.visback,(-800*(g.backx-5),-740*g.backy))
    elif g.backx<5:
        g.visback=g.floors[1]
        g.screen.blit(g.visback,(-800*g.backx,-740*g.backy))
    if g.backx==-1:
        g.floorbound=g.insidehouse[g.backx][g.backy]
    elif g.backx==-2:
        g.floorbound=g.coliseum[g.backx+1][g.backy]
    else:
        g.floorbound=g.housemask[g.backx][g.backy]
    
        
    
def loadMap(fname):#sirs 2d list modded
    lis=[]
    for i in fname:
        
        myPFile = open(i, "rb")        # load my board that I pickled
        lis.append(pickle.load(myPFile))
    return lis
    

def drawall(): #the function that draws everything                    
    if g.backx==-1:#based on the background it subsurfaces so that i dont have to blit every time
        
        g.visback=g.floors[2]
        g.allsprites.clear(g.screen,g.visback.subsurface(0,0,800,740))
    if g.backx==-2:
        g.visback=g.floors[3]
        g.allsprites.clear(g.screen,g.visback.subsurface(0,0,800,740))
        
    if g.backx>4:
        g.visback=g.floors[0]
        g.allsprites.clear(g.screen,g.visback.subsurface(800*(g.backx-5),740*g.backy,800,740))

        
    elif g.backx<5 and g.backx>-1:
        g.visback=g.floors[1]
    
        g.allsprites.clear(g.screen,g.visback.subsurface(800*g.backx,740*g.backy,800,740))#did something weird when the background was not blit
    if g.minmaptoggle==1 and g.hasmap:
        drawminmap()
    settings()
    updatehearts()
    s.rupeehandling(g.rupeenum)  
  
    showammo()

    g.allsprites.update()
    g.allsprites.draw(g.screen)
    test()#for testing 2dlists collision
    display.flip()    
g=game()#initialize game and shop
s=shopclass(g.screen)


        
        
            
        
    
       
#items
redrupee=[imageload(("images/items/redRupee.png"),0.02)]
greenrupee=[imageload(("images/items/GreenRupee.png"),0.02)]#glob all rupees
heartups=[imageload(("images/items/heart.png"),0.04)]
bomb_up=[imageload(("images/items/bomb.png"),0.2)]
arrow_up=[imageload(("images/items/arrow.jpg"),0.2)]
bosskey=[imageload(("images/items/keys.png"),0.1)]
#b_key1=item(bosskey,"bkey+=1",250,250,(-1,0))
#b_key2=item(bosskey,"bkey+=1",518,502,(5,1))
#b_key3=item(bosskey,"bkey+=1",369,239,(7,4))
#b_key4=item(bosskey,"bkey+=1",454,119,(0,2))
#b_key5=item(bosskey,"bkey+=1",310,688,(1,0))
#b_key6=item(bosskey,"bkey+=1",624,200,(1,2))
#b_key7=item(bosskey,"bkey+=1",505,695,(4,2))
#b_key8=item(bosskey,"bkey+=1",415,126,(9,5))
#bkeys=[b_key1,b_key2,b_key3,b_key4,b_key5,b_key6,b_key7,b_key8]
keysleft=g.lood["keysleft"]

for i in keysleft:
        b_key=item(bosskey,"bkey+=1",i[0],i[1],i[2])
        g.keysprites.add(b_key)

#ui
#with pictures
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
Exit = transform.scale(Exit,(130,55))
ExitHover = transform.scale(ExitHover,(130,55))
ExitRect = Exit.get_rect()
ExitRect.center = g.screen.get_rect().centerx,425
Resume = image.load('images/UI/Resume.png').convert()
ResumeHover = image.load('images/UI/ResumeHover.png').convert()
Resume = transform.scale(Resume,(130,55))
ResumeHover = transform.scale(ResumeHover,(130,55))
ResumeRect = Resume.get_rect()
ResumeRect.center = g.screen.get_rect().centerx,315
SettingsMenuRect = Rect(0,0,150,298-10-ExitRect.bottomright[1]+ExitRect[1]-55+10)
SettingsMenuRect.center = g.screen.get_rect().centerx,g.screen.get_rect().centery#298-20
SaveButton = imageload("images/UI/Save.png",1,False,(255,255,255))
SaveRect = SaveButton.get_rect()
SaveRect.center = (g.screen.get_rect().centerx,SettingsMenuRect.centery)
SaveHover = imageload("images/UI/SaveHover.png",1,False,(255,255,255))
sword = image.load('images/UI/sword.png').convert()
sword.set_colorkey((255,255,255))

boomerang = image.load('images/UI/boomerang.png').convert()
boomerang.set_colorkey((0,0,0))

bow = image.load('images/UI/bow.png').convert()
bow.set_colorkey((255,255,255))

heart = transform.scale(heart,(20,20))
##rupee = transform.scale(rupee,(35,35))
gear = transform.scale(gear,(35,35))
gearhover = transform.scale(gearhover,(35,35))

##gearmask = mask.from_surface(gear)

sword = transform.scale(sword,(75,75))
boomerang = transform.scale(boomerang,(75,75))
bow = transform.scale(bow,(75,75))





gear_rect = Rect(gear.get_rect(x=755,y=10))


def drawminmap():
 
    
    
 
 
 
    if g.backx>4:
        minmap=imageload("images/MinMapLostWoods.png")
        minmap=transform.scale(g.visback,(200,200))
        minmaprect = Rect(600,540,200,200)
          
        
        linkmappos=((link.x+(800*g.backx))*(0.4028125),(link.y+(740*g.backy))*(0.397635135))
        
    else:
        minmap=imageload("images/MinMapMainOverworld.png")
 
        minmaprect = Rect(600,540,200,200)
        linkmappos=((link.x+(800*g.backx*0.4028125))*(0.4028125),(link.y+(740*g.backy*0.397635135))*(0.397635135))
        
    #if g.visback!=g.floors[2] and g.visback!=g.floors[3]:
    draw.rect(ui,(255,215,0),(g.screenx-205,g.screeny-205,minmaprect[2]+5,minmaprect[3]))
    ui.blit(minmap,(g.screenx-200,g.screeny-200))

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
    ui.blit(SaveButton,SaveRect)
    if SaveRect.collidepoint(g.mx,g.my):
        ui.blit(SaveHover,SaveRect)
        if g.mb[0]==1:
            save()
    if change:
        blitback()
 
def showammo():
    draw.rect(ui,(255,215,0),(0,g.screeny-100,65,80))
    draw.rect(ui,(100,100,100),(0,g.screeny-95,60,70))
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

dirnames=["left","right","up","down"]# for naming movements
linkanimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),2,True) for i in glob("images"+sep+"link"+sep+"*") for k in glob(i+sep+"*") }#set key to folder name with pics in a list
sluganimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),2,True) for k in glob("images"+sep+"slug"+sep+"*") }
squidanimations={j:imageload(glob(k+sep+"*.png"),2,True) for k in glob("images"+sep+"squid") for j in dirnames}
chuchuanimations={j:imageload(glob(k+sep+"*.png"),1,True) for k in glob("images"+sep+"chuchu") for j in dirnames}
bombarossaanimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),2,True) for k in glob("images"+sep+"bombenemy"+sep+"*")}

wizzrobeanimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),2,True) for k in glob("images"+sep+"wizzrobe"+sep+"*") }
wizzrobeweaponanimations={"fire":[imageload("images/weapons/wizzrobeweapon/wizzrobeweapon0.png",2)]}
boomeranganimations={"boomer":imageload(glob("images"+sep+"weapons"+sep+"boomerang"+sep+"*.png"),2,True,(0,0,0))}
bombanimations={"bomb":imageload(glob("images"+sep+"weapons"+sep+"bomb"+sep+"*.gif"),1,True)}
bombanimations["bomb"].insert(0,imageload("images"+sep+"weapons"+sep+"bomb"+sep+"0.png",0.45))
minotauranimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),1,True) for i in glob("images"+sep+"fboss"+sep+"*") for k in glob(i+sep+"*") }
redwispanimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),2,True) for k in glob("images"+sep+"redwisp"+sep+"*") }
arrowanimations={"arrowup":[imageload("images/weapons/arrow/arrowup.png",0.5,(41,253,47))],
                 "arrowdown":[imageload("images/weapons/arrow/arrowdown.png",0.5,(41,253,47))],
                 "arrowleft":[imageload("images/weapons/arrow/arrowleft.png",0.5,(41,253,47))],
                 "arrowright":[imageload("images/weapons/arrow/arrowright.png",0.5,(41,253,47))]}
hadieanimations={k.split(sep)[-1]:imageload(glob(k+sep+"*.png"),3.7,True) for k in glob("images"+sep+"hadienemy"+sep+"*") }


#creating class objects
link=zelda(linkanimations,5,g.lood["hearts"],g.lood["posx"],g.lood["posy"],"walkleft")#initialize the characters
boomerang=throwingweap(boomeranganimations,10,200,link.x,link.y,"boomer")
arrow=shootingweap(arrowanimations,10,200,link.x,link.y,"arrowup")

bomb=bombweap(bombanimations,10,200,link.x,link.y,"bomb")

wizzflame=weapon(wizzrobeweaponanimations,6,100,0,0,"fire")
g.enemyweaponsprites.add(wizzflame)
minotaur=boss(minotauranimations,5,45,400,400,(-2,0),"down")

#enemies #going to create enemy spawner from file io later and implement like item creation
#need to replace with for loop
wizzrobe=wizzrob(wizzrobeanimations,5,6,528,368,(2,0),wizzflame,"left")
wizzrobe2=wizzrob(wizzrobeanimations,5,6,425,527,(4,0),wizzflame,"left")
wizzrobe3=wizzrob(wizzrobeanimations,5,6,432,392,(4,2),wizzflame,"left")



#self,startx,starty,rng,location,speed=4,homing=False



for i in range(50,750,100):
    regbullet = sentrybullet(i,50,300,(2,0),7)
    homingbullet = sentrybullet(i,50,300,(2,0),7,True)
    
    




#clock object
clock=time.Clock()

#animation counter for enemies


def loadenemies(file="",speed=0,health=0,ani=False,clas=enemy,iniframe=""):#load enemies from text file
    notani=False
    epos=open(file).read().strip().split("\n")
    epos=[(i.split(" ")) for i in epos]
    poss=[]
    stat=(speed,health)
    if not iniframe:
        iniframe="left"
    if not ani:
        notani=True
        
  
    for i in epos:
     
        if notani:
            
            ani=choice((redwispanimations,sluganimations,squidanimations,chuchuanimations))#chooses randomly and sets stats to which enemy it is
            if ani==chuchuanimations:
                stat=(5,3)
            if ani== sluganimations:
                stat=(7,1)
            if ani==squidanimations:
                stat=(3,4)
            if ani==redwispanimations:
                stat=(1,2)
        pos=(round(float(i[0])),round(float(i[1])),round(float(i[2])),round(float(i[3])))

        enem=clas(ani,stat[0],stat[1],(pos[2],pos[3]),pos[0],pos[1],iniframe)#initializes enemy classes

                

             
loadenemies("enemypos/sscPos.txt")
loadenemies("enemypos/BombarossaPos.txt",5,3,bombarossaanimations,bombarossa)#although bomb enemy has many lives he will explode but more than one is needed so that he doesnt just disappear
loadenemies("enemypos/GrassMobPos.txt",3,5,hadieanimations,hadi,"wakeup")




#event.set_grab(True)
shop=shopclass(g.screen)#initialize
blitback()
#blit the background
key.set_repeat(1,600)#to set intervals
running=True
page="opening"

while running:
 

 
    g.keys=key.get_pressed()
    g.mx,g.my=mouse.get_pos()
    g.mb=mouse.get_pressed()
    clock.tick(40)
   

    for e in event.get():
        
        if e.type == QUIT:
            running = False
        if e.type==KEYDOWN:
     #to make sure its not repetitive keydown is used with the set interval
            if e.key==K_q:
                link.rolling=True
            
           
            if e.key==K_SPACE:
                
                link.slashing=True
        
        if e.type==KEYUP:
        
            
            if link.rolling!=True:
                
                link.reset()
            if e.key==K_m:
               
                g.minmaptoggle*=-1#toggle map
                blitback()
    if page=="opening":
               
               story = open("openingcutscene.txt").read().strip().split("\n")
               opening = scroll(g.screen,story)
               opening.play()
               page="game"
               blitback()
    
            
    if page=="shop":#runs shop then add what you bought to what you have
        shop.rupeenum=g.rupeenum
        add=shop.loop()
        bomb.ammo+=add[1]
        arrow.ammo+=add[2]
        link.health+=add[0]
        link.fairy+=add[3]
        g.hasmap=add[4]
        g.bkey+=add[5]
        g.rupeenum=add[6]
        page="game"
        blitback()
        link.x-=50#so he doesnt activate shop over and over again
        link.frame=0
        link.animate()
        
    if page=="game":
        g.run()#runs the game
        
        drawall()
    
    if page=="settings":    
        settingsmenu()
        display.update()
    if page=="menu":
        page=menu()
        
        blitback()
    
 
    
quit()#not necessary since the player will want to play forever
